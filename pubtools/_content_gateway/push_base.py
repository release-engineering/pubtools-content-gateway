from .cgw_client import CGWClient
from .cgw_authentication import CGWBasicAuth
import logging

LOG = logging.getLogger("pubtools.cgw")
LOG_FORMAT = "%(asctime)s [%(levelname)-8s] %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)


class CGWError(Exception):
    """Custom exception class to handle Content Gateway errors."""

    def __init__(self, msg):
        super(CGWError, self).__init__(msg)


class FetcherDict:
    """A class to fetch the ids of the products, versions and file
    from their mapping object
    """

    def __init__(self, val=None, fetcher=None, key_checker=None):
        """
        Initializing the FetcherDict
        The fetcher takes a fetch method as an argument and returns response.
        The key checker takes a mapping method as an argument and validate its keys.

        Args:
            fetcher (method):
                A fetch method instance
            key_checker (method):
                A mapping method instance
        """

        self.fetcher = fetcher
        self.key_checker = key_checker
        self.data = val or {}

    def __setitem__(self, key, val):
        """
        Set the data value of the specified key

        Args:
            key (tuple):
                Tuple key to set specified value
            val (value):
                Value to be set
        """
        self.key_checker(key)
        self.data[key] = val

    def __getitem__(self, key):
        """
        Returns the data value of the specified key

        Args:
            key (tuple):
                Tuple key to return value

        Returns:
            key (value):
                Returns the value of specified key.
        """

        self.key_checker(key)
        if key not in self.data and self.fetcher:
            for new_key, vid in self.fetcher(*key):
                self.data[new_key] = vid
        return self.data[key]

    def get(self, key, default=None):
        """
        Returns the data value of the specified key

        Args:
            key (tuple):
                Tuple key to return value

        Returns:
            key (value):
                Returns the value of specified key.
        """
        self.key_checker(key)
        if key not in self.data and self.fetcher:
            for new_key, vid in self.fetcher(*key):
                self.data[new_key] = vid
        return self.data.get(key, default)

    def __delitem__(self, key):
        """
        Delete the data value of the specified index

        Args:
            key (tuple):
                Tuple key to delete specified record
        """
        self.key_checker(key)
        self.data.__delitem__(key)


class PushBase:
    """Base class for all operations on content gateway via
    either through entry points or from staged input.

    Adds arguments and environment variables common to all operations.
    """

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
        self.pv_mapping = FetcherDict(
            {},
            fetcher=self._fetch_product_version,
            key_checker=self._product_version_mapping_key_check,
        )
        self.file_mapping = FetcherDict({}, fetcher=self._fetch_file, key_checker=self._file_key_check)
        self.product_records = {}
        self.version_records = {}
        self.file_records = {}
        self.completed_operations = []

    @staticmethod
    def _product_mapping_key_check(key):
        """
        Checks the product mapping keys. The keys must follow the following constraints:
            1) The key must be of tuple type
            2) Two keys must be present in the key tuple

        Args:
            key (tuple(str, str)):
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
        Checks the product version mapping keys. The keys must follow the following constraints:
            1) The key must be of tuple type
            2) Three keys must be present in the key tuple

        Args:
            key (tuple(str, str, str|int)):
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
        Checks the product version mapping keys. The keys must follow the following constraints:
            1) The key must be of tuple type
            2) Four keys must be present in the key tuple

        Args:
            key (tuple(str, str, str|int, str)):
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
            Yields (tuple):
                Returns the product record. The returned structure
                is an iterator.

                Intended to be called as the first operation in
                the content gateway workflow.
        """

        all_products = self.cgw_client.get_products()
        for product in all_products:
            self.product_records[product["id"]] = product
            yield (product["name"], product["productCode"]), product["id"]

    def _fetch_product_version(self, product_name, product_code, version_name):
        """
        Get the list of product versions from the content gateway
        by calling its client methods.

        Args:
            product_name (str):
                product name of the product
            product_code (str):
                product code of the product
            version_name (str|int):
                version name of the product

        Returns:
            Yields (tuple):
                Returns the version records associate with the product.
                The returned structure is an iterator.
        """

        product_id = self.product_mapping.get((product_name, product_code))
        all_versions = self.cgw_client.get_versions(product_id)
        for version in all_versions:
            self.version_records[version["id"]] = version
            yield (product_name, product_code, version["versionName"]), version["id"]

    def _fetch_file(self, product_name, product_code, version_name, download_url):
        """
        Get the list of file records associate with version and product
        from the content gateway by calling its client methods.

        Args:
            product_name (str):
                product name of the file
            product_code (str):
                product code of the file
            version_name (str|int):
                version name of the file
            download_url (str):
                download url of the file

        Returns:
            Yields (dict):
                Returns the file records.
                The returned structure is an iterator.
        """

        product_id = self.product_mapping.get((product_name, product_code))
        version_id = self.pv_mapping.get((product_name, product_code, version_name))
        all_files = self.cgw_client.get_files(product_id, version_id)
        for data in all_files:
            self.file_records[data["id"]] = data
            yield (
                product_name,
                product_code,
                version_name,
                data["downloadURL"],
            ), data.get("id")

    def process_product(self, item):
        """
        Responsible for product workflow operations such as Create,
        Update and delete the product based on the satisfied condition.

        The product operation follows the following workflow:
            - Search for the product record from the product mapping
            - If `product action` == `create`

                - Creates a new product record on content gateway with given data
                - Add the new record into the product mapping records

            - If `product action` == `update` and record found in mapping or id is provided in metadata

                - Update the product record on content gateway with given data
                - Update the record into the product mapping records

            - If `product action` == `delete` and record found in mapping or id is provided in metadata

                - Delete the product record on the content gateway
                - Remove the record from the product mapping records

            - If `product action` == `delete` or `update` and record not found in mapping

                - Raises CGWError error

        Args:
            item (dict):
                Metadata of product record

        Raises:
            CGWError:
                When product record is not present and tries to update/delete the same

        Returns:
            product_id (int):
                Returns the product ID
        """

        product_name = item.get("metadata").get("name")
        product_code = item.get("metadata").get("productCode")
        LOG.debug(
            "Fetching for product_id of product_name:- %s and product_code:- %s \n" % (product_name, product_code)
        )

        #  Trying to fetch product_id from CGW mapping.
        product_id = self.product_mapping.get((product_name, product_code))

        #  If CGW mapping doesn't have the record it will try to get product_id from metadata if provided
        #  For the create operation it will not get any product_id either from the CGW
        #  or from metadata. The product_id would be None
        #  To update the product name and productCode the product_id must be provided in the metadata
        product_id = product_id if product_id else item.get("metadata").get("id")

        if item.get("action") == "create":
            if product_id:
                LOG.error(
                    "Record already present for the product name:- %s and code:- %s and product_id is %s "
                    % (product_name, product_code, product_id)
                )
                raise CGWError("Cannot create new product. Record already present.")

            product_id = self.cgw_client.create_product(item.get("metadata"))
            # A new product is created so updating the existing product mapping
            self.product_mapping[(product_name, product_code)] = product_id
            LOG.info("Created a new product with product_id:- %s\n" % product_id)

            # adding operational product_id for rollback operation
            item["product_id"] = product_id
            # keeping a copy of data that has been used to create the cgw data
            self.completed_operations.append(item)
            return product_id

        elif item.get("action") == "update" and product_id:
            item.get("metadata")["id"] = product_id
            LOG.info("Updating product record of id:- %s \n", product_id)
            self.cgw_client.update_product(item.get("metadata"))

            # keeping a copy of data that has been used to update the cgw data
            self.completed_operations.append(item)

        elif item.get("action") == "delete" and product_id:
            LOG.info("Deleting existing product records for product_id:- %s" % product_id)
            self.cgw_client.delete_product(product_id)
            del self.product_mapping[(product_name, product_code)]

            #  removing the deleted file record from the completed operations
            #  this is to avoid the conflicts during the rollback and make_visible operations
            for record in self.completed_operations:
                if record["type"] == "product" and record["product_id"] == product_id:
                    self.completed_operations.remove(record)

            LOG.info("Product record deleted! \n")
        else:
            raise CGWError("Cannot update/delete the product %s %s, id is not set" % (product_name, product_code))
        return product_id

    def process_version(self, item):
        """
        Responsible for version workflow operations such as Create,
        Update and delete the product version based on the satisfied condition
        on content gateway (CGW).

        The product version operation follows the following workflow:
            - Search for the product record from the product mapping
            - Search for the product version record from the product_version(pv_mapping) mapping
            - If `version action` == `create`

                - Creates a new version record associated with product on CGW with given data
                - Add the new record into the mapping records

            - If `version action` == `update` and record found in mapping or id is provided in metadata

                - Update the version record on content gateway with given data
                - Update the record into the version mapping records

            - If `version action` == `delete` and record found in mapping or id is provided in metadata

                - Delete the version record on the content gateway
                - Remove the record from the version mapping records

            - If `version action` == `delete` or `update` and record not found in mapping
               or id is not provided in metadata

                - Raises CGWError error

        Args:
            item (dict):
                Metadata of version record

        Raises:
            CGWError:
                - When product record is not present
                - When version record is not present and tries to update/delete the same

        Returns:
            version_id (int|None):
                Returns the version ID
        """

        product_name = item.get("metadata")["productName"]
        product_code = item.get("metadata")["productCode"]
        version_name = item.get("metadata")["versionName"]

        product_id = self.product_mapping.get((product_name, product_code))
        if not product_id:
            raise CGWError("Product name: %s product code: %s not found" % (product_name, product_code))

        LOG.debug(
            "Fetching the product and version_id of "
            "product_name:- %s and version_name:- %s \n" % (product_name, version_name)
        )

        #  Trying to fetch version_id from CGW mapping.
        version_id = self.pv_mapping.get((product_name, product_code, version_name))

        #  If CGW mapping doesn't have the record it will try to get version_id from metadata if provided
        #  For the create operation it will not get any version_id either from the CGW
        #  or from metadata. The version_id would be None
        #  To update the versionName the version_id must be provided in the metadata
        version_id = version_id if version_id else item.get("metadata").get("id")

        item.get("metadata")["productId"] = product_id
        del item.get("metadata")["productName"], item.get("metadata")["productCode"]

        if item.get("action") == "create":
            if version_id:
                LOG.error(
                    "Record already present for the version name:- %s and code:- %s and version_id is %s "
                    % (version_name, product_code, version_id)
                )
                raise CGWError("Cannot create new version. Record already present.")
            LOG.info("Creating version entry for the given version_name: %s ", version_name)
            version_id = self.cgw_client.create_version(product_id, item.get("metadata"))
            # adding new version record to the version mapping
            self.pv_mapping[(product_name, product_code, version_name)] = version_id
            LOG.info("New version created with version_id:- %s \n" % version_id)

            # adding operational version_id for rollback operation
            item["version_id"] = version_id
            # keeping a copy of data that has been used to create the cgw data
            self.completed_operations.append(item)
            return

        if item.get("action") == "update" and version_id:
            item.get("metadata")["id"] = version_id
            LOG.info("Updating the version metadata \n")
            self.cgw_client.update_version(product_id, item.get("metadata"))
            # keeping a copy of data that has been used to update the cgw data
            self.completed_operations.append(item)

        elif item.get("action") == "delete" and version_id:
            LOG.info("Deleting existing version records for version_id:- %s" % version_id)
            self.cgw_client.delete_version(product_id, version_id)
            del self.pv_mapping[(product_name, product_code, version_name)]

            #  removing the deleted file record from the completed operations
            #  this is to avoid the conflicts during the rollback and make_visible operations
            for record in self.completed_operations:
                if record["type"] == "product_version" and record["version_id"] == version_id:
                    self.completed_operations.remove(record)

            LOG.info("Version record deleted! \n")
        else:
            raise CGWError(
                "Cannot update/delete the version name: '%s' product code: '%s' product: '%s', id is not set"
                % (version_name, product_code, product_name)
            )
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
            - If `file action` == `create`

                - Creates a new file record associated with product on CGW with given data
                - Add the new record into the file mapping records

            - If `file action` == `update` and record found in mapping or id is provided in metadata

                - Update the file record on content gateway with given data
                - Update the record into the file mapping records

            - If `file action` == `delete` and record found in mapping or id is provided in metadata

                - Delete the file record on the content gateway
                - Remove the record from the file mapping records

            - If `file action` == `delete` or `update` and record not found in mapping
              or id is not provided in metadata

                - Raises CGWError error

            - The default file `order` value will be `10` if provided none
            - file `order` will be auto incremented by `10` for nested data yml structure

        Args:
            file_item (dict):
                Metadata of file record

        Raises:
            CGWError:
                - When product record is not present
                - When version record is not present
                - When file record is not present and tries to update/delete the same

        Returns:
            file_id (int|None):
                Returns the file ID
        """

        LOG.debug("Fetching file id for the file metadata \n")
        product_name = file_item.get("metadata").get("productName")
        product_code = file_item.get("metadata").get("productCode")
        version_name = file_item.get("metadata").get("productVersionName")
        download_url = file_item.get("metadata").get("downloadURL")
        product_id = self.product_mapping.get((product_name, product_code))

        if not product_id:
            raise CGWError("Product name: %s product code: %s not found" % (product_name, product_code))

        version_id = self.pv_mapping.get((product_name, product_code, version_name))
        if not version_id:
            raise CGWError(
                "Product name: %s product code: %s version name: %s not found"
                % (product_name, product_code, version_name)
            )

        #  Trying to fetch file_id from CGW mapping.
        file_id = self.file_mapping.get((product_name, product_code, version_name, download_url))

        #  If CGW mapping doesn't have the record it will try to get file_id from metadata if provided
        #  For the create operation it will not get any file_id neither from the CGW
        #  nor from metadata. The file_id would be None
        #  To update the downloadURL the file_id must be provided in the metadata
        file_id = file_id if file_id else file_item.get("metadata").get("id")

        del (
            file_item.get("metadata")["productName"],
            file_item.get("metadata")["productCode"],
            file_item.get("metadata")["productVersionName"],
        )
        file_item.get("metadata")["productVersionId"] = version_id

        if file_item.get("action") == "create":
            if file_id:
                LOG.error(
                    "Record already present for the file download_url :- %s and file_id is %s "
                    % (download_url, file_id)
                )
                raise CGWError("Cannot create new file. Record already present.")
            LOG.info("Creating file entry for the given downloadURL: %s ", download_url)
            file_metadata = file_item.get("metadata")
            if "pushItemPath" in file_metadata:
                file_metadata.pop("pushItemPath")
            file_id = self.cgw_client.create_file(product_id, version_id, file_metadata)
            self.file_mapping[(product_name, product_code, version_name, download_url)] = file_id
            LOG.info("New file created with file_id:- %s \n" % file_id)

            # adding operational product_id and file_id for rollback operation
            file_item["product_id"] = product_id
            file_item["file_id"] = file_id
            # keeping a copy of data that has been used to create the cgw data
            self.completed_operations.append(file_item)
            return

        if file_item.get("action") == "update" and file_id:
            LOG.info("Updating the file record \n")
            file_item.get("metadata")["id"] = file_id
            self.cgw_client.update_file(product_id, version_id, file_item.get("metadata"))

            # adding operational product_id for rollback operation
            file_item["product_id"] = product_id
            # keeping a copy of data that has been used to update the cgw data
            self.completed_operations.append(file_item)

        elif file_item.get("action") == "delete" and file_id:
            LOG.info("Deleting existing file records for file_id:- %s" % file_id)
            self.cgw_client.delete_file(product_id, version_id, file_id)

            #  removing the deleted file record from the completed operations
            #  this is to avoid the conflicts during the rollback and make_visible operations
            for record in self.completed_operations:
                if record["type"] == "file" and record["file_id"] == file_id:
                    self.completed_operations.remove(record)

            LOG.info("File record deleted! \n")
            del self.file_mapping[(product_name, product_code, version_name, download_url)]
        else:
            raise CGWError(
                "Cannot update/delete file: product version: '%s' product code: '%s' product: '%s', id is not set"
                % (version_name, product_code, product_name)
            )
        return file_id

    def make_visible(self):
        """

        - Update the invisible attribute to False.
          once all the CGW operation completed successfully.

        - This is needed to make the version and file records visible.
        - The `invisible` attribute changes on the following conditions:

            - `invisible=True` :- sets if user externally specify the `invisible=True`
            - `invisible=False` :- sets either if user externally specify the `invisible=False`
              or user doesn't specify any value for this `invisible` attribute.

        """

        LOG.debug("Updating the invisible attribute of the created records")
        LOG.debug("Enabling the created records if required \n")

        self.completed_operations.reverse()
        for item in self.completed_operations:
            if item.get("type") == "product_version":
                if item.get("action") == "create":
                    item["metadata"]["id"] = item["version_id"]
                    item["metadata"]["invisible"] = False if not item["metadata"].get("invisible") else True
                    self.cgw_client.update_version(item["metadata"]["productId"], item["metadata"])

            elif item.get("type") == "file":
                if item.get("action") == "create":
                    item["metadata"]["id"] = item["file_id"]
                    item["metadata"]["invisible"] = False if not item["metadata"].get("invisible") else True
                    self.cgw_client.update_file(
                        item["product_id"],
                        item["metadata"]["productVersionId"],
                        item["metadata"],
                    )

    def rollback_cgw_operation(self):
        """

        Undo the partial completed CGW operation.
            - For the create operations it will delete the created data from CGW
            - For the update operation it will revert the changes with old data.

        """

        self.completed_operations.reverse()
        for item in self.completed_operations:
            if item.get("type") == "product":
                if item.get("action") == "create":
                    self.cgw_client.delete_product(item["product_id"])
                    LOG.info("Rollback done for created product:- %s", item["product_id"])

                elif item.get("action") == "update":
                    item["metadata"] = self.product_records.get(item["metadata"]["id"])
                    self.cgw_client.update_product(item["metadata"])
                    LOG.info("Rollback done for updated product:- %s", item["metadata"]["id"])

            elif item.get("type") == "product_version":
                if item.get("action") == "create":
                    self.cgw_client.delete_version(item["metadata"]["productId"], item["version_id"])
                    LOG.info(
                        "Rollback done for created product_version:- %s",
                        item["version_id"],
                    )

                elif item.get("action") == "update":
                    item["metadata"] = self.version_records.get(item["metadata"]["id"])
                    self.cgw_client.update_version(item["metadata"]["productId"], item["metadata"])
                    LOG.info(
                        "Rollback done for updated product_version:- %s",
                        item["metadata"]["id"],
                    )

            elif item.get("type") == "file":
                if item.get("action") == "create":
                    self.cgw_client.delete_file(
                        item["product_id"],
                        item["metadata"]["productVersionId"],
                        item["file_id"],
                    )
                    LOG.info("Rollback done for created file:- %s", item["file_id"])

                elif item.get("action") == "update":
                    item["metadata"] = self.file_records.get(item["metadata"]["id"])
                    self.cgw_client.update_file(
                        item["product_id"],
                        item["metadata"]["productVersionId"],
                        item["metadata"],
                    )
                    LOG.info("Rollback done for updated file:- %s", item["metadata"]["id"])
        LOG.info("Rollback operations completed...!")
