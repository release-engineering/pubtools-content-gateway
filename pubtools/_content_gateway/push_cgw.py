import argparse
from .cgw_client import *
from .cgw_authentication import CGWBasicAuth
from .utils import yaml_parser, validate_schema
import logging

LOG = logging.getLogger("pubtools.cgw")
LOG_FORMAT = "%(asctime)s [%(levelname)-8s] %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)


class PushCGW:
    def __init__(self, cgw_hostname, cgw_username, cgw_password, cgw_filepath):
        self.auth = CGWBasicAuth(cgw_username, cgw_password)
        self.cgw_client = CGWClient(cgw_hostname, self.auth)
        self.cgw_filepath = cgw_filepath
        self.product_mapping = None
        self.pv_mapping = None

    def _create_product_version_mapping(self, product_name, product_code):
        product_id = self._get_product_id(product_name, product_code)
        all_versions = self.cgw_client.get_versions(product_id)
        self.pv_mapping = {(product_name, product_code, data.get('versionName')): (product_id, data.get('id')) for data
                           in all_versions}

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
        file_mapping = {(product_name, product_code, version_name, data.get('downloadURL')): (
            product_id, version_id, data.get('id')) for data in all_files}
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
                  "product name:- %s and version name:- %s" % (product_id, version_name))
        version_id = self._get_version_id(product_name, product_code, version_name)

        if item.get('state') == 'present':
            item.get('metadata')['productId'] = product_id
            del item.get('metadata')['productName'], item.get('metadata')['productCode']
            if not version_id:
                LOG.info("No previous entries found for the given product's version")
                LOG.info("Creating version entry for the given version metadata")
                version_id = self.cgw_client.create_version(product_id, item.get('metadata'))
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

    def cgw_operations(self):
        # Parsing yaml file
        cgw_items = yaml_parser(self.cgw_filepath)
        # Creating product mapping to get the product_id with name and productCode
        cgw_products = self.cgw_client.get_products()
        # All the mappings will get removed when we will update/delete the products/versions and files by ids
        self.product_mapping = {(data['name'], data['productCode']): data['id'] for data in cgw_products}
        for item in cgw_items:
            is_validated = validate_schema(item)
            if item['type'] == 'product' and is_validated:
                self.process_product(item)
            elif item['type'] == 'product_version' and is_validated:
                if not self.pv_mapping:
                    self._create_product_version_mapping(item.get('metadata')['productName'],
                                                          item.get('metadata')['productCode'])
                self.process_version(item)
            elif item['type'] == 'file' and is_validated:
                self.process_file(item)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-host", "--CGW_hostname",
                        required=True,
                        metavar="CGW-hostname",
                        help="Hostname of the server")
    parser.add_argument("-u", "--CGW_username",
                        required=True,
                        metavar="CGW-username",
                        help="Username of Content Gateway")
    # TODO: Reading password form the environment variable if it's set
    parser.add_argument("-p", "--CGW_password",
                        metavar="CGW-password",
                        help="Password for Content Gateway")
    parser.add_argument("-f", "--CGW_filepath",
                        required=True,
                        metavar="CGW-filepath",
                        help="File path to read metadata")
    args = parser.parse_args()
    push_cgw = PushCGW(args.CGW_hostname, args.CGW_username, args.CGW_password, args.CGW_filepath)
    push_cgw.cgw_operations()
