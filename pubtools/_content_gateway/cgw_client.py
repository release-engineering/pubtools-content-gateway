import json
from .cgw_session import CGWSession


class CGWClientError(Exception):
    """
    Custom exception to handle Content Gateway Client errors
    """

    def __init__(self, message):
        self.message = message


class CGWClient:
    def __init__(self, hostname, cgw_auth=None, verify=True):
        self.hostname = hostname
        # Check if CGW hostname is present
        if not self.hostname:
            raise CGWClientError("No content gateway hostname found")
        self.hostname = hostname.rstrip("/")
        self.cgw_session = CGWSession(self.hostname, verify=verify)
        if cgw_auth:
            cgw_auth.make_auth(self.cgw_session)

    def call_cgw_api(self, method, endpoint, params=None, data=None):

        # Check if correct method id passed
        if method not in ["GET", "POST", "PUT", "DELETE"]:
            raise CGWClientError("Wrong request method passed")

        response = None
        output = {}
        try:
            if method == "GET":
                response = self.cgw_session.get(endpoint, params=params)
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
            raise CGWClientError("content gateway API returned error: "
                                 "\nstatus_code: %s, reason: %s, error: %s"
                                 % (response.status_code, response.reason, response.text))

        if response.text:
            output = response.json()
        return output

    def get_products(self, params=None):
        resp_data = self.call_cgw_api("GET", '/products', params=params)
        return resp_data

    def get_product(self, pid, params=None):
        endpoint = "/products/%s" % pid
        resp_data = self.call_cgw_api("GET", endpoint, params=params)
        return resp_data

    def create_product(self, data):
        endpoint = "/products/"
        resp_data = self.call_cgw_api("PUT", endpoint, data=json.dumps(data))
        return resp_data

    def update_product(self, data):
        endpoint = "/products"
        resp_data = self.call_cgw_api("POST", endpoint, data=json.dumps(data))
        return resp_data

    def delete_product(self, pid, params=None):
        endpoint = "/products/%s" % pid
        resp_data = self.call_cgw_api("DELETE", endpoint, params=params)
        return resp_data

    def get_versions(self, pid, params=None):
        endpoint = "/products/%s/versions" % pid
        resp_data = self.call_cgw_api("GET", endpoint, params=params)
        return resp_data

    def get_version(self, pid, vid, params=None):
        endpoint = "/products/%s/versions/%s" % (pid, vid)
        resp_data = self.call_cgw_api("GET", endpoint, params=params)
        return resp_data

    def create_version(self, pid, data):
        endpoint = "/products/%s/versions/" % pid
        resp_data = self.call_cgw_api("PUT", endpoint, data=json.dumps(data))
        return resp_data

    def update_version(self, pid, data):
        endpoint = "/products/%s/versions" % pid
        resp_data = self.call_cgw_api("POST", endpoint, data=json.dumps(data))
        return resp_data

    def delete_version(self, pid, vid, params=None):
        endpoint = "/products/%s/versions/%s" % (pid, vid)
        resp_data = self.call_cgw_api("DELETE", endpoint, params=params)
        return resp_data

    def get_all_files(self, pid, vid, params=None):
        endpoint = "/products/%s/versions/%s/all" % (pid, vid)
        resp_data = self.call_cgw_api("GET", endpoint, params=params)
        return resp_data

    def get_files(self, pid, vid, params=None):
        endpoint = "/products/%s/versions/%s/files" % (pid, vid)
        resp_data = self.call_cgw_api("GET", endpoint, params=params)
        return resp_data

    def get_file(self, pid, vid, fid, params=None):
        endpoint = "/products/%s/versions/%s/files/%s" % (pid, vid, fid)
        resp_data = self.call_cgw_api("GET", endpoint, params=params)
        return resp_data

    def create_file(self, pid, vid, data):
        endpoint = "/products/%s/versions/%s/files" % (pid, vid)
        resp_data = self.call_cgw_api("PUT", endpoint, data=json.dumps(data))
        return resp_data

    def update_file(self, pid, vid, data):
        endpoint = "/products/%s/versions/%s/files" % (pid, vid)
        resp_data = self.call_cgw_api("POST", endpoint, data=json.dumps(data))
        return resp_data

    def delete_file(self, pid, vid, fid, data=None):
        endpoint = "/products/%s/versions/%s/files/%s" % (pid, vid, fid)
        resp_data = self.call_cgw_api("DELETE", endpoint, data=data)
        return resp_data

    def get_urls(self, pid, vid, data=None):
        endpoint = "/products/%s/versions/%s/urls" % (pid, vid)
        resp_data = self.call_cgw_api("GET", endpoint, data=data)
        return resp_data

    def get_url(self, pid, vid, uid, data=None):
        endpoint = "/products/%s/versions/%s/urls/%s" % (pid, vid, uid)
        resp_data = self.call_cgw_api("GET", endpoint, data=data)
        return resp_data

    def create_url(self, pid, vid, data):
        endpoint = "/products/%s/versions/%s/urls/" % (pid, vid)
        resp_data = self.call_cgw_api("PUT", endpoint, data=json.dumps(data))
        return resp_data

    def update_url(self, pid, vid, data):
        endpoint = "/products/%s/versions/%s/urls/" % (pid, vid)
        resp_data = self.call_cgw_api("POST", endpoint, data=json.dumps(data))
        return resp_data

    def delete_url(self, pid, vid, uid, data=None):
        endpoint = "/products/%s/versions/%s/urls/%s" % (pid, vid, uid)
        resp_data = self.call_cgw_api("DELETE", endpoint, data=data)
        return resp_data

    def get_internals(self, pid, vid, data=None):
        endpoint = "/products/%s/versions/%s/internals" % (pid, vid)
        resp_data = self.call_cgw_api("GET", endpoint, data=data)
        return resp_data

    def get_internal(self, pid, vid, uid, data=None):
        endpoint = "/products/%s/versions/%s/internals/%s" % (pid, vid, uid)
        resp_data = self.call_cgw_api("GET", endpoint, data=data)
        return resp_data

    def create_internal(self, pid, vid, data):
        endpoint = "/products/%s/versions/%s/internal/" % (pid, vid)
        resp_data = self.call_cgw_api("PUT", endpoint, data=json.dumps(data))
        return resp_data

    def update_internal(self, pid, vid, data):
        endpoint = "/products/%s/versions/%s/internal/" % (pid, vid)
        resp_data = self.call_cgw_api("POST", endpoint, data=json.dumps(data))
        return resp_data

    def delete_internal(self, pid, vid, uid, data=None):
        endpoint = "/products/%s/versions/%s/internal/%s" % (pid, vid, uid)
        resp_data = self.call_cgw_api("DELETE", endpoint, data=data)
        return resp_data
