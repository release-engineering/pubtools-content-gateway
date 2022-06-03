from pushsource import Source, CGWPushItem
from .cgw_client import *
from .cgw_authentication import CGWBasicAuth
from .utils import yaml_parser, validate_schema
import logging

LOG = logging.getLogger("pubtools.cgw")
LOG_FORMAT = "%(asctime)s [%(levelname)-8s] %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)


class PushStagedCGW:
    def __init__(self, push_items, hub, task_id, target_name, target_settings):
        self.auth = CGWBasicAuth(target_settings['username'], target_settings['password'])
        self.cgw_client = CGWClient(target_settings['server_name'], self.auth)
        self.product_mapping = None
        self.pv_mapping = None

        self.push_items = push_items
        self.hub = hub
        self.task_id = task_id
        self.target_name = target_name

    def __create_product_version_mapping(self, product_name, product_code):
        product_id = self.__get_product_id(product_name, product_code)
        all_versions = self.cgw_client.get_versions(product_id)
        self.pv_mapping = {(product_name, product_code, data.get('versionName')): (product_id, data.get('id')) for data
                           in all_versions}

    def __get_product_id(self, product_name, product_code):
        product_id = self.product_mapping.get((product_name, product_code))
        return product_id

    def __get_version_id(self, product_name, product_code, version_name):
        version_id = self.pv_mapping.get((product_name, product_code, version_name)) if self.pv_mapping else None
        if version_id:
            _, version_id = version_id
        return version_id

    def __get_file_id(self, file_item):
        product_name = file_item.get('metadata').get('productName')
        product_code = file_item.get('metadata').get('productCode')
        version_name = file_item.get('metadata').get('productVersionName')

        product_id = self.__get_product_id(product_name, product_code)
        if not self.pv_mapping:
            self.__create_product_version_mapping(product_name, product_code)
        version_id = self.__get_version_id(product_name, product_code, version_name)
        all_files = self.cgw_client.get_files(product_id, version_id)
        file_mapping = {(product_name, product_code, version_name, data.get('downloadURL')): (
            product_id, version_id, data.get('id')) for data in all_files}
        pvf_id = file_mapping.get(
            (product_name, product_code, version_name,
             file_item.get('metadata').get('downloadURL'))) if file_mapping else (None, None, None)
        return pvf_id

    def process_product(self, item):
        try:
            product_name = item.get('metadata').get('name')
            product_code = item.get('metadata').get('productCode')
            LOG.debug(f"Fetching for product_id of product name- {product_name} and product code- {product_code}")
            product_id = self.__get_product_id(product_name, product_code)

            if item.get('state') == 'present':
                if not product_id:
                    LOG.info("No previous entries found for the given product name and product code")
                    LOG.info("Creating product entry for the given product metadata")
                    product_id = self.cgw_client.create_product(item.get('metadata'))
                    # A new product is created so updating product mapping
                    cgw_data = self.cgw_client.get_products()
                    self.product_mapping = {(data['name'], data['productCode']): data['id'] for data in cgw_data}
                    LOG.debug(f"Created a new product with product_id:- {product_id}")
                    return
                LOG.info(f"Product record found with product_id:- {product_id}")
                item.get('metadata')['id'] = product_id
                LOG.info("Updating product metadata")
                self.cgw_client.update_product(item.get('metadata'))
            elif item.get('state') == 'absent' and product_id:
                LOG.info(f"Deleting existing product records for product_id:- {product_id}")
                self.cgw_client.delete_product(product_id)
                LOG.info("Product record deleted!")
            else:
                LOG.warning("Invalid state or metadata!")
        except Exception as err:
            LOG.exception(err)

    def process_version(self, item):
        try:
            product_name = item.get('metadata')['productName']
            product_code = item.get('metadata')['productCode']
            version_name = item.get('metadata')['versionName']
            product_id = self.__get_product_id(product_name, product_code)
            LOG.debug(f"Fetching the product and version id of "
                      f"product name- {product_name} and version name- {version_name}")
            version_id = self.__get_version_id(product_name, product_code, version_name)

            if item.get('state') == 'present':
                item.get('metadata')['productId'] = product_id
                del item.get('metadata')['productName'], item.get('metadata')['productCode']
                if not version_id:
                    LOG.info("No previous entries found for the given product's version")
                    LOG.info("Creating version entry for the given version metadata")
                    version_id = self.cgw_client.create_version(product_id, item.get('metadata'))
                    self.__create_product_version_mapping(product_name, product_code)
                    LOG.info(f"New version created with version_id:- {version_id}")
                    return
                item.get('metadata')['id'] = version_id
                LOG.info(f"Found version record with version_id:- {version_id}")
                LOG.info("Updating the version metadata")
                self.cgw_client.update_version(product_id, item.get('metadata'))
            elif item.get('state') == 'absent' and version_id:
                LOG.info(f"Deleting existing version records for version_id:- {version_id}")
                self.cgw_client.delete_version(product_id, version_id)
                LOG.info("Version record deleted!")
            else:
                LOG.warning("Invalid state or metadata!")
        except Exception as error:
            LOG.exception(error)

    def process_file(self, file_item):
        try:
            product_id, version_id, file_id = self.__get_file_id(file_item)
            LOG.debug(f"Fetching file id for the file metadata")
            if not (product_id and version_id):
                product_name = file_item.get('metadata').get('productName')
                product_code = file_item.get('metadata').get('productCode')
                version_name = file_item.get('metadata').get('productVersionName')
                product_id = self.__get_product_id(product_name, product_code)
                version_id = self.__get_version_id(product_name, product_code, version_name)

            if file_item.get('state') == 'present':
                del file_item.get('metadata')['productName'], \
                    file_item.get('metadata')['productCode'], \
                    file_item.get('metadata')['productVersionName']
                file_item.get('metadata')['productVersionId'] = version_id
                for item in self.push_items:
                    if item.metadata['file_path'] == file_item['metadata']['pushItemPath']:
                        file_item['metadata']['size'] = item.metadata['file_size']
                        file_item['metadata']['md5'] = item.metadata['md5']
                        file_item['metadata']['sha256'] = item.metadata['sha256']
                        # item2.file_info['metadata']['checksums']['sha256']
                        # TODO: Update te download url dest_path
                        file_item['metadata']['downloadURL'] = item.metadata['dest_path']

                if not file_id:
                    LOG.info("No previous entries found for the given file metadata")
                    LOG.info("Creating version entry for the given file metadata")
                    file_id = self.cgw_client.create_file(product_id, version_id, file_item.get('metadata'))
                    LOG.info(f"New file created with file_id:- {file_id}")
                    return
                LOG.info(f"Found file record with file_id:- {file_id}")
                LOG.info("Updating the file metadata")
                file_item.get('metadata')['id'] = file_id
                self.cgw_client.update_file(product_id, version_id, file_item.get('metadata'))
            elif file_item.get('state') == 'absent' and file_id:
                LOG.info(f"Deleting existing file records for file_id:- {file_id}")
                self.cgw_client.delete_file(product_id, version_id, file_id)
                LOG.info("File record deleted!")
            else:
                LOG.warning("Invalid state or metadata!")
        except Exception as error:
            LOG.exception(error)

    def push_staged_operations(self):
        cgw_products = self.cgw_client.get_products()
        for item in self.push_items:
            if isinstance(item, CGWPushItem):
                parsed_items = yaml_parser(item.src)
                self.product_mapping = {(data.get('name'), data.get('productCode')): data.get('id') for data in
                                        cgw_products}
                for pitem in parsed_items:
                    if pitem['type'] == 'product':
                        if not validate_schema(pitem):
                            continue
                        self.process_product(pitem)
                    if pitem.get('type') == 'product_version':
                        if not validate_schema(pitem):
                            continue
                        if not self.pv_mapping:
                            self.__create_product_version_mapping(pitem.get('metadata')['productName'],
                                                                pitem.get('metadata')['productCode'])
                        self.process_version(pitem)
                    if pitem['type'] == 'file':
                        if not validate_schema(pitem):
                            continue
                        self.process_file(pitem)


def entry_point(push_items, hub, task_id, target_name, target_settings):
    push_staged = PushStagedCGW(push_items, hub, task_id, target_name, target_settings)
    push_staged.push_staged_operations()
