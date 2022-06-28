from pushsource import CGWPushItem
from .cgw_client import *
from .cgw_authentication import CGWBasicAuth
from .utils import yaml_parser, validate_schema
import logging
from attrs import asdict
import pluggy
import json

pm = pluggy.PluginManager("pubtools")
hookspec = pluggy.HookspecMarker("pubtools")
hookimpl = pluggy.HookimplMarker("pubtools")

LOG = logging.getLogger("pubtools.cgw")
LOG_FORMAT = "%(asctime)s [%(levelname)-8s] %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)


class PushStagedCGW:
    def __init__(self, target_name, target_settings):
        self.auth = CGWBasicAuth(target_settings['username'], target_settings['password'])
        self.cgw_client = CGWClient(target_settings['server_name'], self.auth)
        self.product_mapping = {}
        self.pv_mapping = {}
        self.push_items = []
        self.target_name = target_name
        self.pulp_push_items = {}

    def _create_product_version_mapping(self, product_name, product_code):
        product_id = self._get_product_id(product_name, product_code)
        all_versions = self.cgw_client.get_versions(product_id)
        for data in all_versions:
            self.pv_mapping[(product_name, product_code, data.get('versionName'))] = (product_id, data.get('id'))

    def _get_product_id(self, product_name, product_code):
        product_id = self.product_mapping.get((product_name, product_code))
        return product_id

    def _get_version_id(self, product_name, product_code, version_name):
        version_id = self.pv_mapping.get((product_name, product_code, version_name)) if self.pv_mapping else None
        if version_id:
            _, version_id = version_id
        return version_id

    def _get_file_id(self, file_item):
        product_name = file_item.get('metadata').get('productName')
        product_code = file_item.get('metadata').get('productCode')
        version_name = file_item.get('metadata').get('productVersionName')

        product_id = self._get_product_id(product_name, product_code)
        if not self.pv_mapping:
            self._create_product_version_mapping(product_name, product_code)
        version_id = self._get_version_id(product_name, product_code, version_name)
        all_files = self.cgw_client.get_files(product_id, version_id)
        file_mapping = {}
        for data in all_files:
            file_mapping[(product_name, product_code, version_name, data.get('downloadURL'))] = (
                product_id, version_id, data.get('id'))
        pvf_id = file_mapping.get(
            (product_name, product_code, version_name,
             file_item.get('metadata').get('downloadURL'))) if file_mapping else (None, None, None)
        return pvf_id

    def process_product(self, item):
        product_name = item.get('metadata').get('name')
        product_code = item.get('metadata').get('productCode')
        LOG.debug(
            "Fetching for product_id of product name:- %s and product code:- %s" % (product_name, product_code))
        product_id = self._get_product_id(product_name, product_code)

        if item.get('state') == 'present':
            if not product_id:
                LOG.info("No previous entries found for the given product name and product code")
                LOG.info("Creating product entry for the given product metadata")
                product_id = self.cgw_client.create_product(item.get('metadata'))
                # A new product is created so updating the existing product mapping
                self.product_mapping[(product_name, product_code)] = product_id

                LOG.debug("Created a new product with product_id:- %s" % product_id)
                return
            LOG.info("Product record found with product_id:- %s" % product_id)
            item.get('metadata')['id'] = product_id
            LOG.info("Updating product metadata")
            self.cgw_client.update_product(item.get('metadata'))
        elif item.get('state') == 'absent' and product_id:
            LOG.info("Deleting existing product records for product_id:- %s" % product_id)
            self.cgw_client.delete_product(product_id)
            LOG.info("Product record deleted!")

    def process_version(self, item):
        product_name = item.get('metadata')['productName']
        product_code = item.get('metadata')['productCode']
        version_name = item.get('metadata')['versionName']
        product_id = self._get_product_id(product_name, product_code)
        LOG.debug("Fetching the product and version id of "
                  "product name:- %s and version name:- %s" % (product_name, version_name))
        version_id = self._get_version_id(product_name, product_code, version_name)

        if item.get('state') == 'present':
            item.get('metadata')['productId'] = product_id
            del item.get('metadata')['productName'], item.get('metadata')['productCode']
            if not version_id:
                LOG.info("No previous entries found for the given product's version")
                LOG.info("Creating version entry for the given version metadata")
                version_id = self.cgw_client.create_version(product_id, item.get('metadata'))
                # adding new version record to the version mapping
                self.pv_mapping[(product_name, product_code, version_name)] = (product_id, version_id)
                LOG.info("New version created with version_id:- %s" % version_id)
                return
            item.get('metadata')['id'] = version_id
            LOG.info("Found version record with version_id:- %s" % version_id)
            LOG.info("Updating the version metadata")
            self.cgw_client.update_version(product_id, item.get('metadata'))
        elif item.get('state') == 'absent' and version_id:
            LOG.info("Deleting existing version records for version_id:- %s" % version_id)
            self.cgw_client.delete_version(product_id, version_id)
            LOG.info("Version record deleted!")

    def process_file(self, file_item):
        product_id, version_id, file_id = self._get_file_id(file_item)
        LOG.debug("Fetching file id for the file metadata")
        if not (product_id and version_id):
            product_name = file_item.get('metadata').get('productName')
            product_code = file_item.get('metadata').get('productCode')
            version_name = file_item.get('metadata').get('productVersionName')
            product_id = self._get_product_id(product_name, product_code)
            version_id = self._get_version_id(product_name, product_code, version_name)

        if file_item.get('state') == 'present':
            del file_item.get('metadata')['productName'], \
                file_item.get('metadata')['productCode'], \
                file_item.get('metadata')['productVersionName']
            file_item.get('metadata')['productVersionId'] = version_id

            for item in self.push_items:
                if item.metadata['file_path'] == file_item['metadata']['pushItemPath']:
                    file_item['metadata']['size'] = item.metadata['file_size']
                    file_item['metadata']['md5'] = item.metadata['md5sum']
                    file_item['metadata']['sha256'] = item.metadata['sha256sum']
                    file_item['metadata']['downloadURL'] = self.pulp_push_items[
                        json.dumps(asdict(self.push_item), sort_keys=True)].cdn_path

            if not file_id:
                LOG.info("No previous entries found for the given file metadata")
                LOG.info("Creating version entry for the given file metadata")
                file_id = self.cgw_client.create_file(product_id, version_id, file_item.get('metadata'))
                LOG.info("New file created with file_id:- %s" % file_id)
                return
            LOG.info("Found file record with file_id:- %s" % file_id)
            LOG.info("Updating the file metadata")
            file_item.get('metadata')['id'] = file_id
            self.cgw_client.update_file(product_id, version_id, file_item.get('metadata'))
        elif file_item.get('state') == 'absent' and file_id:
            LOG.info("Deleting existing file records for file_id:- %s" % file_id)
            self.cgw_client.delete_file(product_id, version_id, file_id)
            LOG.info("File record deleted!")

    def push_staged_operations(self):
        cgw_products = self.cgw_client.get_products()
        for item in self.push_items:
            if isinstance(item, CGWPushItem):
                parsed_items = yaml_parser(item.src)
                for data in cgw_products:
                    self.product_mapping[(data['name'], data['productCode'])] = data['id']
                for pitem in parsed_items:
                    is_validated = validate_schema(pitem)
                    if pitem['type'] == 'product' and is_validated:
                        self.process_product(pitem)
                    if pitem.get('type') == 'product_version' and is_validated:
                        if not self.pv_mapping:
                            self._create_product_version_mapping(pitem.get('metadata')['productName'],
                                                                 pitem.get('metadata')['productCode'])
                        self.process_version(pitem)
                    if pitem['type'] == 'file' and is_validated:
                        self.process_file(pitem)

    @hookimpl
    def gather_source_items(self, pulp_push_item, push_item):
        self.push_item = push_item
        self.pulp_push_items[json.dumps(asdict(self.push_item), sort_keys=True)] = pulp_push_item


def entry_point(target_name, target_settings):
    push_staged = PushStagedCGW(target_name, target_settings)
    return push_staged
