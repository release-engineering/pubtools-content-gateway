from .cgw_client import CGWClient
from .cgw_authentication import CGWBasicAuth
import logging

LOG = logging.getLogger("pubtools.cgw")
LOG_FORMAT = "%(asctime)s [%(levelname)-8s] %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)


class CGWError(Exception):
    """
    Custom exception class to handle Content Gateway errors
    """

    def __init__(self, msg):
        super(CGWError, self).__init__(msg)


class FetcherDict:
    """ A class to fetch the ids of the products, versions and file
        from their mapping object
    """

    def __init__(self, val=None, fetcher=None, key_checker=None):
        """Initializing the FetcherDict"""
        self.fetcher = fetcher
        self.key_checker = key_checker
        self.data = val or {}

    def __setitem__(self, key, val):
        """Set the data value of the specified index"""
        self.key_checker(key)
        self.data[key] = val

    def __getitem__(self, key):
        """Returns the data value of the specified index"""
        self.key_checker(key)
        if key not in self.data and self.fetcher:
            for new_key, vid in self.fetcher(*key):
                self.data[new_key] = vid
        return self.data[key]

    def get(self, key, default=None):
        """Returns the data value of the specified index"""
        self.key_checker(key)
        if key not in self.data and self.fetcher:
            for new_key, vid in self.fetcher(*key):
                self.data[new_key] = vid
        return self.data.get(key, default)

    def __delitem__(self, key):
        """Delete the data value of the specified index"""
        self.key_checker(key)
        self.data.__delitem__(key)


class PushBase:
    """Base class for all operations on content gateway via
    either through entry points or from staged input.

    Adds arguments and environment variables common to all operations.
    """

    @staticmethod
    def _product_mapping_key_check(key):
        """
        Checks the product mapping keys.
        The keys must follow the following constraints:
            1) The key must be of tuple type
            2) Two keys must be present in the key tuple

        Args:
            key (tuple(int, int)):
                The keys should contain product, product_code

        Raises:
            ValueError:
                When the keys are not of tuple type or
                the keys in tuple doesn't satisfy the length size.
        """

        if not isinstance(key, tuple):
            raise ValueError("key must be tuple (product, product_code)")
        elif not len(key) == 2:
            raise ValueError("key must be tuple (product, product_code)")

    @staticmethod
    def _product_version_mapping_key_check(key):
        """
        Checks the product version mapping keys.
        The keys must follow the following constraints:
            1) The key must be of tuple type
            2) Three keys must be present in the key tuple

        Args:
            key (tuple(int, int, int)):
                The keys should contain product, product_code and product_version

        Raises:
            ValueError:
                When the keys are not of tuple type or
                the keys in tuple doesn't satisfy the length size.
        """

        if not isinstance(key, tuple):
            raise ValueError("key must be tuple (product, product_code, product_version)")
        elif not len(key) == 3:
            raise ValueError("key must be tuple (product, product_code, product_version)")

    @staticmethod
    def _file_key_check(key):
        """
        Checks the product version mapping keys.
        The keys must follow the following constraints:
            1) The key must be of tuple type
            2) Four keys must be present in the key tuple

        Args:
            key (tuple(int, int, int)):
                The keys should contain product, product_code,
                 product_version and downloadURL

        Raises:
            ValueError:
                When the keys are not of tuple type or
                the keys in tuple doesn't satisfy the length size.
        """

        if not isinstance(key, tuple):
            raise ValueError("key must be tuple (product, product_code, product_version, downloadURL)")
        elif not len(key) == 4:
            raise ValueError("key must be tuple (product, product_code, product_version, downloadURL)")

    def _fetch_product(self, product_name, product_code):
        """
        Get the list of products from the content gateway
        by calling its client methods.

        Args:
            product_name (str):
                product name of the product
            product_code (str):
                product code of the product

        Returns:
            Yields (dict):
                Returns the product record. The returned structure
                is an iterator to reduce memory requirements.

                Intended to be called as the first operation in
                the content gateway workflow.
        """

        all_products = self.cgw_client.get_products()
        for product in all_products:
            yield (product['name'], product['productCode']), product['id']

    def _fetch_product_version(self, product_name, product_code, version_name):
        """
        Get the list of product versions from the content gateway
        by calling its client methods.

        Args:
            product_name (str):
                product name of the product
            product_code (str):
                product code of the product
            version_name (str):
                version name of the product

        Returns:
            Yields (dict):
                Returns the version records associate with the product.
                The returned structure is an iterator to reduce memory requirements.
        """

        product_id = self.product_mapping.get((product_name, product_code))
        all_versions = self.cgw_client.get_versions(product_id)
        for version in all_versions:
            yield (product_name, product_code, version['versionName']), version['id']

    def _fetch_file(self, product_name, product_code, version_name, download_url):
        """
        Get the list of file records associate with version and product
        from the content gateway by calling its client methods.

        Args:
            product_name (str):
                product name of the file
            product_code (str):
                product code of the file
            version_name (str):
                version name of the file
            download_url (str):
                download url of the file

        Returns:
            Yields (dict):
                Returns the file records.
                The returned structure is an iterator to reduce memory requirements.
        """

        product_id = self.product_mapping.get((product_name, product_code))
        version_id = self.pv_mapping.get((product_name, product_code, version_name))
        all_files = self.cgw_client.get_files(product_id, version_id)
        for data in all_files:
            yield (product_name, product_code, version_name, data['downloadURL']), data.get('id')

    def __init__(self, cgw_hostname, cgw_username, cgw_password):
        """
        Initialize.

        Args:
            cgw_hostname (str):
                CGW registry URL
            cgw_username (str):
                username for CGW HTTP API
            cgw_password (str):
                password for CGW HTTP API
        """

        self.auth = CGWBasicAuth(cgw_username, cgw_password)
        self.cgw_client = CGWClient(cgw_hostname, self.auth)
        self.product_mapping = FetcherDict({}, fetcher=self._fetch_product, key_checker=self._product_mapping_key_check)
        self.pv_mapping = FetcherDict({}, fetcher=self._fetch_product_version,
                                      key_checker=self._product_version_mapping_key_check)
        self.file_mapping = FetcherDict({}, fetcher=self._fetch_file, key_checker=self._file_key_check)

    def process_product(self, item):
        """
        Responsible for product workflow operations such as Create,
        Update and delete the product based on the satisfied condition.

        The product operation follows the following workflow:
            - Search for the product record from the product mapping
            - If `product state` == `present` and record not found in mapping

                - Creates a new product record on content gateway with given data
                - Add the new record into the product mapping records

            - If `product state` == `present` and record found in mapping

                - Update the product record on content gateway with given data
                - Update the record into the product mapping records

            - If `product state` == `absent` and record found in mapping

                - Delete the product record on the content gateway
                - Remove the record from the product mapping records

            - If `product state` == `absent` and record not found in mapping

                - Raises CGWError error

        Args:
            item (list(dict)):
                List of product record

        Raises:
            CGWError:
                When product record is not present and tries to delete the same

        Returns:
            product_id (int):
                Returns the product ID
        """

        product_name = item.get('metadata').get('name')
        product_code = item.get('metadata').get('productCode')
        LOG.debug(
            "Fetching for product_id of product_name:- %s and product_code:- %s" % (product_name, product_code))

        product_id = self.product_mapping.get((product_name, product_code))

        if item.get('state') == 'present':
            if not product_id:
                LOG.info("No previous entries found for the given product name and product code")
                LOG.info("Creating product entry for the given product metadata")
                product_id = self.cgw_client.create_product(item.get('metadata'))
                # A new product is created so updating the existing product mapping
                self.product_mapping[(product_name, product_code)] = product_id
                LOG.info("Created a new product with product_id:- %s" % product_id)
                return product_id

            LOG.info("Product record found with product_id:- %s" % product_id)
            item.get('metadata')['id'] = product_id
            LOG.info("Updating product metadata")
            self.cgw_client.update_product(item.get('metadata'))
        elif item.get('state') == 'absent' and product_id:
            LOG.info("Deleting existing product records for product_id:- %s" % product_id)
            self.cgw_client.delete_product(product_id)
            del self.product_mapping[(product_name, product_code)]
            LOG.info("Product record deleted!")
        else:
            raise CGWError("Cannot delete the product %s %s, id is not set" % (product_name, product_code))
        return product_id

    def process_version(self, item):
        """
        Responsible for version workflow operations such as Create,
        Update and delete the product version based on the satisfied condition
        on content gateway (CGW).

        The product version operation follows the following workflow:
            - Search for the product record from the product mapping
            - Search for the product version record from the product_version(pv_mapping) mapping
            - If `version state` == `present` and record not found in mapping

                - Creates a new version record associated with product on CGW with given data
                - Add the new record into the mapping records

            - If `version state` == `present` and record found in mapping

                - Update the version record on content gateway with given data
                - Update the record into the version mapping records

            - If `version state` == `absent` and record found in mapping

                - Delete the version record on the content gateway
                - Remove the record from the version mapping records

            - If `version state` == `absent` and record not found in mapping

                - Raises CGWError error

        Args:
            item (list(dict)):
                List of version record

        Raises:
            CGWError:
                When version record is not present and tries to delete the same

        Returns:
            version_id (int|None):
                Returns the version ID
        """

        product_name = item.get('metadata')['productName']
        product_code = item.get('metadata')['productCode']
        version_name = item.get('metadata')['versionName']

        product_id = self.product_mapping.get((product_name, product_code))
        if not product_id:
            raise CGWError("Product name: %s product code: %s not found" % (product_name, product_code))

        LOG.debug("Fetching the product and version_id of "
                  "product_name:- %s and version_name:- %s" % (product_name, version_name))

        version_id = self.pv_mapping.get((product_name, product_code, version_name))
        if item.get('state') == 'present':
            item.get('metadata')['productId'] = product_id
            del item.get('metadata')['productName'], item.get('metadata')['productCode']
            if not version_id:
                LOG.info("No previous entries found for the given product's version")
                LOG.info("Creating version entry for the given version_name: %s ", version_name)
                version_id = self.cgw_client.create_version(product_id, item.get('metadata'))
                # adding new version record to the version mapping
                self.pv_mapping[(product_name, product_code, version_name)] = version_id
                LOG.info("New version created with version_id:- %s" % version_id)
                return

            item.get('metadata')['id'] = version_id
            LOG.info("Found version record with version_id:- %s" % version_id)
            LOG.info("Updating the version metadata")
            self.cgw_client.update_version(product_id, item.get('metadata'))
        elif item.get('state') == 'absent' and version_id:
            LOG.info("Deleting existing version records for version_id:- %s" % version_id)
            self.cgw_client.delete_version(product_id, version_id)
            del self.pv_mapping[(product_name, product_code, version_name)]
            LOG.info("Version record deleted!")
        else:
            raise CGWError("Cannot delete the version name: '%s' product code: '%s' product: '%s', id is not set" %
                           (version_name, product_code, product_name))
        return version_id

    def process_file(self, file_item):
        """
        Responsible for file workflow operations such as Create,
        Update and delete the file based on the satisfied condition
        on content gateway (CGW).

        The file operation follows the following workflow:
            - Search for the product record from the product mapping
            - Search for the product version record from the product_version (pv_mapping) mapping
            - Search for the file record from the file mapping (file_mapping) mapping
            - If `file state` == `present` and record not found in mapping

                - Creates a new file record associated with product on CGW with given data
                - Add the new record into the file mapping records

            - If `file state` == `present` and record found in mapping

                - Update the file record on content gateway with given data
                - Update the record into the file mapping records

            - If `file state` == `absent` and record found in mapping

                - Delete the file record on the content gateway
                - Remove the record from the file mapping records

            - If `file state` == `absent` and record not found in mapping

                - Raises CGWError error

        Args:
            file_item (list(dict)):
                List of file record

        Raises:
            CGWError:
                When file record is not present and tries to delete the same

        Returns:
            file_id (int|None):
                Returns the file ID
        """

        LOG.debug("Fetching file id for the file metadata")
        product_name = file_item.get('metadata').get('productName')
        product_code = file_item.get('metadata').get('productCode')
        version_name = file_item.get('metadata').get('productVersionName')
        download_url = file_item.get('metadata').get('downloadURL')
        product_id = self.product_mapping.get((product_name, product_code))

        if not product_id:
            raise CGWError("Product name: %s product code: %s not found" % (product_name, product_code))

        version_id = self.pv_mapping.get((product_name, product_code, version_name))
        if not version_id:
            raise CGWError("Product name: %s product code: %s version name: %s not found" % (
                product_name, product_code, version_name))

        file_id = self.file_mapping.get((product_name, product_code, version_name, download_url))

        if file_item.get('state') == 'present':
            del file_item.get('metadata')['productName'], \
                file_item.get('metadata')['productCode'], \
                file_item.get('metadata')['productVersionName']
            file_item.get('metadata')['productVersionId'] = version_id

            if not file_id:
                LOG.info("No previous entries found for the given file metadata")
                LOG.info("Creating file entry for the given downloadURL: %s ", download_url)
                file_id = self.cgw_client.create_file(product_id, version_id, file_item.get('metadata'))
                self.file_mapping[
                    (product_name, product_code, version_name, download_url)] = file_id
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
            del self.file_mapping[(product_name, product_code, version_name, download_url)]
        else:
            raise CGWError("Cannot delete file: product version: '%s' product code: '%s' product: '%s', id is not set" %
                           (version_name, product_code, product_name))
        return file_id
