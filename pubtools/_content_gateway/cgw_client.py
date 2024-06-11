import json
from .cgw_session import CGWSession


class CGWClientError(Exception):
    """Custom exception class to handle Content Gateway Client errors"""

    def __init__(self, message):
        self.message = message


class CGWClient:
    """Class for performing content gateway HTTP API operations."""

    def __init__(self, hostname, cgw_auth=None, verify=True):
        """
        Initialize.

        Args:
            hostname (str):
                CGW host URL.
            cgw_auth (CGWBasicAuth):
                CGWBasicAuth subclass instance
            verify (bool)
                enable/disable SSL verification

        """

        self.hostname = hostname
        # Check if CGW hostname is present
        if not self.hostname:
            raise CGWClientError("No content gateway hostname found")
        self.hostname = hostname.rstrip("/")
        self.cgw_session = CGWSession(self.hostname, verify=verify)
        if cgw_auth:
            cgw_auth.make_auth(self.cgw_session)

    def call_cgw_api(self, method, endpoint, data=None):
        """
        Perform an HTTP API request on content gateway registry.

        Args:
            method (str):
                REST API method of the request (GET, POST, PUT, DELETE).
            endpoint (str):
                Endpoint of the request.
            data (dict):
                Optional arguments for the method Request object.

        Returns (list|dict|int):
            Returns either list or dict response for GET method
            and int for PUT methods.

        Raises:
            CGWClientError: When the request returns an error status.
            Exception: Occurs if API call fails.
        """

        # Check if correct method id passed
        if method not in ["GET", "POST", "PUT", "DELETE"]:
            raise CGWClientError("Wrong request method passed")

        response = None
        output = {}
        try:
            if method == "GET":
                response = self.cgw_session.get(endpoint, data=data)
            elif method == "POST":
                response = self.cgw_session.post(endpoint, data=data)
            elif method == "PUT":
                response = self.cgw_session.put(endpoint, data=data)
            elif method == "DELETE":
                response = self.cgw_session.delete(endpoint)
        except Exception as e:
            msg = "Error: Exception occurred during API call: %s" % str(e)
            raise CGWClientError(msg)

        if not response.ok:
            raise CGWClientError(
                "content gateway API returned error: "
                "\nstatus_code: %s, reason: %s, error: %s" % (response.status_code, response.reason, response.text)
            )

        if response.text:
            output = response.json()
        return output

    def get_products(self):
        """
        Get list of all products.

        Returns (list[dict]):
            Returns list of products.
        """

        resp_data = self.call_cgw_api("GET", "/products")
        return resp_data

    def get_product(self, pid):
        """
        Get one product record specified by its identifier.

        Args:
            pid (int):
                product id of requested product

        Returns (dict):
            Returns the requested product.
        """

        endpoint = "/products/%s" % pid
        resp_data = self.call_cgw_api("GET", endpoint)
        return resp_data

    def create_product(self, data):
        """
        Creates a new product record on the content gateway.

        Args:
            data (dict):
                product data to be created

        Returns (int):
            Returns the created product id.
        """

        endpoint = "/products/"
        resp_data = self.call_cgw_api("PUT", endpoint, data=json.dumps(data))
        return resp_data

    def update_product(self, data):
        """
        Updates an existing product record.

        Args:
            data (dict):
                product data to be updated

        Returns (dict):
            Returns empty dict on successful product update.
        """

        endpoint = "/products"
        resp_data = self.call_cgw_api("POST", endpoint, data=json.dumps(data))
        return resp_data

    def delete_product(self, pid):
        """
        Attempts to delete an existing product record.
        It is not possible to delete products,
        that has any product versions.

        Args:
            pid (int):
                product id of the record that need to be deleted

        Returns (dict):
            Returns empty dict on successful product delete.
        """

        endpoint = "/products/%s" % pid
        resp_data = self.call_cgw_api("DELETE", endpoint)
        return resp_data

    def get_versions(self, pid):
        """
        Get list of versions belonging to the specific product.

        Args:
            pid (int):
                product id of the version

        Returns (list[dict]):
            Returns a list of a specific product versions
        """

        endpoint = "/products/%s/versions" % pid
        resp_data = self.call_cgw_api("GET", endpoint)
        return resp_data

    def get_version(self, pid, vid):
        """
        Get one product version record specified by its identifier.

        Args:
            pid (int):
                product id of the version
            vid (int):
                requested version id

        Returns (dict):
           A single version record.
        """

        endpoint = "/products/%s/versions/%s" % (pid, vid)
        resp_data = self.call_cgw_api("GET", endpoint)
        return resp_data

    def create_version(self, pid, data):
        """
        Creates a new product version record on the content gateway.

        Args:
            pid (int):
                product id for which version needs to be created
            data (dict):
                version data to be created

        Returns (int):
            Returns the created version id.
        """
        endpoint = "/products/%s/versions/" % pid
        resp_data = self.call_cgw_api("PUT", endpoint, data=json.dumps(data))
        return resp_data

    def update_version(self, pid, data):
        """
        Updates an existing version record.

        Args:
            pid (int):
                product id of the version
            data (dict):
                version data to be updated

        Returns (dict):
            Returns empty dict on successful version update.
        """

        endpoint = "/products/%s/versions" % pid
        resp_data = self.call_cgw_api("POST", endpoint, data=json.dumps(data))
        return resp_data

    def delete_version(self, pid, vid):
        """
        Attempts to delete an existing version record.
        It is not possible to delete a version,
        that has any file records.

        Args:
            pid (int):
                product id of the version
            vid (int):
                version id of the record that need to be deleted

        Returns (dict):
            Returns empty dict on successful version delete.
        """

        endpoint = "/products/%s/versions/%s" % (pid, vid)
        resp_data = self.call_cgw_api("DELETE", endpoint)
        return resp_data

    def get_all_files(self, pid, vid):
        """
        Get list of all files, links and internal links of the specific version.

        Args:
            pid (int):
                product id of the file
            vid (int):
                version id of the file

        Returns (list[dict]):
            Returns a list of a specific product version files
        """

        endpoint = "/products/%s/versions/%s/all" % (pid, vid)
        resp_data = self.call_cgw_api("GET", endpoint)
        return resp_data

    def get_files(self, pid, vid):
        """
        Get list of files belonging to the specific product version.

        Args:
            pid (int):
                product id of the file
            vid (int):
                version id of the file

        Returns (list[dict]):
            Returns a list of a specific product version files
        """

        endpoint = "/products/%s/versions/%s/files" % (pid, vid)
        resp_data = self.call_cgw_api("GET", endpoint)
        return resp_data

    def get_file(self, pid, vid, fid):
        """
        Get a single file specified by its identifier.

        Args:
            pid (int):
                product id of the file
            vid (int):
                version id of the file
            fid (int):
                requested file id

        Returns (dict):
           A single file record.
        """

        endpoint = "/products/%s/versions/%s/files/%s" % (pid, vid, fid)
        resp_data = self.call_cgw_api("GET", endpoint)
        return resp_data

    def create_file(self, pid, vid, data):
        """
        Creates a new file record on the content gateway.

        Args:
            pid (int):
                product id of the file
            vid (int):
                version id for which file needs to be created
            data (dict):
                file data to be created

        Returns (int):
            Returns the created file id.
        """

        endpoint = "/products/%s/versions/%s/files" % (pid, vid)
        resp_data = self.call_cgw_api("PUT", endpoint, data=json.dumps(data))
        return resp_data

    def update_file(self, pid, vid, data):
        """
        Updates an existing file record.

        Args:
            pid (int):
                product id of the file
            vid (int):
                version id for which file needs to be updated
            data (dict):
                file data to be updated

        Returns (dict):
            Returns empty dict on successful file update.
        """

        endpoint = "/products/%s/versions/%s/files" % (pid, vid)
        resp_data = self.call_cgw_api("POST", endpoint, data=json.dumps(data))
        return resp_data

    def delete_file(self, pid, vid, fid):
        """
        Attempts to delete an existing file record.

        Args:
            pid (int):
                product id of the file
            vid (int):
                version id of the file
            fid (int):
                file id of the record that need to be deleted

        Returns (dict):
            Returns empty dict on successful file delete.
        """

        endpoint = "/products/%s/versions/%s/files/%s" % (pid, vid, fid)
        resp_data = self.call_cgw_api("DELETE", endpoint)
        return resp_data

    def get_urls(self, pid, vid):
        """
        Get list of urls belonging to the specific product version.

        Args:
            pid (int):
                product id of the url
            vid (int):
                version id of the url

        Returns (list[dict]):
            Returns a list of a specific product version urls
        """

        endpoint = "/products/%s/versions/%s/urls" % (pid, vid)
        resp_data = self.call_cgw_api("GET", endpoint)
        return resp_data

    def get_url(self, pid, vid, uid):
        """
        Get a single url specified by its identifier.

        Args:
            pid (int):
                product id of the url
            vid (int):
                version id of the url
            uid (int):
                requested url id

        Returns (dict):
           A single url record.
        """

        endpoint = "/products/%s/versions/%s/urls/%s" % (pid, vid, uid)
        resp_data = self.call_cgw_api("GET", endpoint)
        return resp_data

    def create_url(self, pid, vid, data):
        """
        Creates a new url record on the content gateway.

        Args:
            pid (int):
                product id of the url
            vid (int):
                version id for which url needs to be created
            data (dict):
                url data to be created

        Returns (int):
            Returns the created url id.
        """

        endpoint = "/products/%s/versions/%s/urls/" % (pid, vid)
        resp_data = self.call_cgw_api("PUT", endpoint, data=json.dumps(data))
        return resp_data

    def update_url(self, pid, vid, data):
        """
        Updates an existing url record.

        Args:
            pid (int):
                product id of the url
            vid (int):
                version id for which url needs to be updated
            data (dict):
                url data to be updated

        Returns (dict):
            Returns empty dict on successful url update.
        """

        endpoint = "/products/%s/versions/%s/urls" % (pid, vid)
        resp_data = self.call_cgw_api("POST", endpoint, data=json.dumps(data))
        return resp_data

    def delete_url(self, pid, vid, uid):
        """
        Attempts to delete an existing url record.

        Args:
            pid (int):
                product id of the version
            vid (int):
                version id of the url
            uid (int):
                url id of the record that need to be deleted

        Returns (dict):
            Returns empty dict on successful url delete.
        """

        endpoint = "/products/%s/versions/%s/urls/%s" % (pid, vid, uid)
        resp_data = self.call_cgw_api("DELETE", endpoint)
        return resp_data

    def get_internals(self, pid, vid):
        """
        Get list of internals belonging to the specific product version.

        Args:
            pid (int):
                product id of the internals
            vid (int):
                version id of the internals

        Returns (list[dict]):
            Returns a list of a specific product version internals
        """

        endpoint = "/products/%s/versions/%s/internals" % (pid, vid)
        resp_data = self.call_cgw_api("GET", endpoint)
        return resp_data

    def get_internal(self, pid, vid, iid):
        """
        Get a single internal specified by its identifier.

        Args:
            pid (int):
                product id of the internal
            vid (int):
                version id of the internal
            iid (int):
                requested internal id

        Returns (dict):
           A single internal record.
        """

        endpoint = "/products/%s/versions/%s/internals/%s" % (pid, vid, iid)
        resp_data = self.call_cgw_api("GET", endpoint)
        return resp_data

    def create_internal(self, pid, vid, data):
        """
        Creates a new internal record on the content gateway.

        Args:
            pid (int):
                product id of the internal
            vid (int):
                version id for which internal needs to be created
            data (dict):
                internal data to be created

        Returns (int):
            Returns the created internal id.
        """

        endpoint = "/products/%s/versions/%s/internals/" % (pid, vid)
        resp_data = self.call_cgw_api("PUT", endpoint, data=json.dumps(data))
        return resp_data

    def update_internal(self, pid, vid, data):
        """
        Updates an existing internal record.

        Args:
            pid (int):
                product id of the internal
            vid (int):
                version id for which internal needs to be updated
            data (dict):
                internal data to be updated

        Returns (dict):
            Returns empty dict on successful internal update.
        """

        endpoint = "/products/%s/versions/%s/internals/" % (pid, vid)
        resp_data = self.call_cgw_api("POST", endpoint, data=json.dumps(data))
        return resp_data

    def delete_internal(self, pid, vid, iid):
        """
        Attempts to delete an existing internal record.

        Args:
            pid (int):
                product id of the internal
            vid (int):
                version id of the internal
            iid (int):
                url id of the record that need to be deleted

        Returns (dict):
            Returns empty dict on successful internal delete.
        """

        endpoint = "/products/%s/versions/%s/internals/%s" % (pid, vid, iid)
        resp_data = self.call_cgw_api("DELETE", endpoint)
        return resp_data
