import json
from .cgw_authentication import CGWBasicAuth
from .cgw_session import CGWSession

class CGWClientError(Exception):
    """
    Custom exception to handle Content Gateway Client errors
    """

    def __init__(self, message):
        self.message = message


class CGWClient:
    def __init__(self, hostname, cgw_auth=None, verify=True):
        self.hostname = hostname.rstrip("/")
        self.cgw_session = CGWSession(self.hostname)
        if cgw_auth:
            cgw_auth.make_auth(self.cgw_session)

    def call_cgw_api(self, method, endpoint, params=None, data=None):
        # Check if CGW hostname is present
        if not self.hostname:
            raise CGWClientError("No content gateway hostname found")

        # Check if correct method id passed
        if method not in ["GET", "POST", "PATCH", "PUT", "DELETE"]:
            raise CGWClientError("Wrong request method passed")

        response = None
        output = True
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
            raise CGWClientError("content gateway API returned error: \nstatus_code: %s, reason: %s, error: %s"
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

    def create_product(self, data=None):
        endpoint = "/products/"
        resp_data = self.call_cgw_api("PUT", endpoint, data=json.dumps(data))
        return resp_data

    def update_product(self, pid, data=None):
        # Not working
        endpoint = "/products/%s" % pid
        resp_data = self.call_cgw_api("PUT", endpoint, data=json.dumps(data))
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

    def create_version(self, pid, data=None):
        endpoint = "/products/%s/versions/" % (pid)
        resp_data = self.call_cgw_api("PUT", endpoint, data=json.dumps(data))
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

    def create_file(self, pid, vid, data=None):
        endpoint = "/products/%s/versions/%s/files" % (pid, vid)
        resp_data = self.call_cgw_api("PUT", endpoint, data=json.dumps(data))
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

    def create_url(self, pid, vid, data=None):
        endpoint = "/products/%s/versions/%s/urls/" % (pid, vid)
        resp_data = self.call_cgw_api("PUT", endpoint, data=json.dumps(data))
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

    def create_internal(self, pid, vid, data=None):
        endpoint = "/products/%s/versions/%s/internal/" % (pid, vid)
        resp_data = self.call_cgw_api("PUT", endpoint, data=json.dumps(data))
        return resp_data

    def delete_internal(self, pid, vid, uid, data=None):
        endpoint = "/products/%s/versions/%s/internal/%s" % (pid, vid, uid)
        resp_data = self.call_cgw_api("DELETE", endpoint, data=data)
        return resp_data


# NOTE: Will move these to test module and these unit test will be removed from here
# Please Ignore the unit test for now
def test_cgw_client():
    username = ""
    password = ""

    auth = CGWBasicAuth(username, password)

    hostname = ""
    cgw_client = CGWClient(hostname, auth)

    def test_get_products():
        # Get all products
        try:
            response = cgw_client.get_products()
        except CGWClientError as e:
            CGWClientError("\nError: %s" % str(e))
            return False
        return response

    def test_get_product():
        # Get a particular product using node PID
        pid = 4009704
        try:
            response = cgw_client.get_product(pid)
        except CGWClientError as e:
            CGWClientError("\nError: %s" % str(e))
            return False
        return response

    def test_create_product():
        data = {
            "name": "Cloud: Virtualization Sandbox testing",
            "eloquaCode": "70160000000wxTzAAI"
        }

        try:
            response = cgw_client.create_product(data)
        except CGWClientError as e:
            CGWClientError("\nError: %s" % str(e))
            return False
        return response

    def test_update_product():
        # not implemented
        pass

    def test_delete_product():
        # Get a particular product using node PID
        pid = 4009744
        try:
            response = cgw_client.delete_product(pid)
        except CGWClientError as e:
            CGWClientError("\nError: %s" % str(e))
            return False
        return response

    def test_get_versions():
        # Get all products
        pid = 4009704
        try:
            response = cgw_client.get_versions(pid)
        except CGWClientError as e:
            CGWClientError("\nError: %s" % str(e))
            return False
        return response

    def test_get_version():
        pid = 4009704
        vid = 4154947
        try:
            response = cgw_client.get_version(pid, vid)
        except CGWClientError as e:
            CGWClientError("\nError: %s" % str(e))
            return False
        return response

    def test_create_version():
        data = {
            "productId": 4009704,
            "versionName": "v4",
            "termsAndConditions": "Basic user account"
        }
        pid = 4009704
        try:
            response = cgw_client.create_version(pid, data)
        except CGWClientError as e:
            CGWClientError("\nError: %s" % str(e))
            return False
        return response

    def test_delete_version():
        pid = 4009704
        vid = 4154947
        try:
            response = cgw_client.delete_version(pid, vid)
        except CGWClientError as e:
            CGWClientError("\nError: %s" % str(e))
            return False
        return response

    def test_get_all_files():
        pid = 4009704
        vid = 4154776
        try:
            response = cgw_client.get_all_files(pid, vid)
        except CGWClientError as e:
            CGWClientError("\nError: %s" % str(e))
            return False
        return response

    def test_get_files():
        pid = 4009704
        vid = 4154939
        try:
            response = cgw_client.get_files(pid, vid)
        except CGWClientError as e:
            CGWClientError("\nError: %s" % str(e))
            return False
        return response

    def test_get_file():
        pid = 4009704
        vid = 4154939
        fid = 3871798
        try:
            response = cgw_client.get_file(pid, vid, fid)
        except CGWClientError as e:
            CGWClientError("\nError: %s" % str(e))
            return False
        return response

    def test_create_file():
        data = {
            "description": "Red Hat OpenShift Local Sandbox",
            "label": "Checksum File Sandbox",
            "order": 0,
            "hidden": 0,
            "invisible": 0,
            "modifiedBy": "R: Jalam@redhat.com",
            "productVersionId": 4154939,
            "type": "FILE",
            "downloadURL": "/content/origin/files/sha256/92/92327795758e76095ee4868935bc2b62ee464eed96abbf604845191448b549df/sha256sum",
            "shortURL": "/pub-5/openshift-v4/clients/ansibletest/1.99.4/sha256sum"
        }
        pid = 4009704
        vid = 4154939

        try:
            response = cgw_client.create_file(pid, vid, data)
        except CGWClientError as e:
            CGWClientError("\nError: %s" % str(e))
            return False
        return response

    def test_delete_file():
        pid = 4009704
        vid = 4154939
        fid = 3871835
        try:
            response = cgw_client.delete_file(pid, vid, fid)
        except CGWClientError as e:
            CGWClientError("\nError: %s" % str(e))
            return False
        return response

    def test_get_urls():
        pid = 4009704
        vid = 4154741
        try:
            response = cgw_client.get_urls(pid, vid)
        except CGWClientError as e:
            CGWClientError("\nError: %s" % str(e))
            return False
        return response

    def test_get_url():
        pid = 4009704
        vid = 4154741
        uid = 3869885
        try:
            response = cgw_client.get_url(pid, vid, uid)
        except CGWClientError as e:
            CGWClientError("\nError: %s" % str(e))
            return False
        return response

    def test_create_url():
        data = {
            "description": "Sandbox URL",
            "label": "Sandbox URL Testing",
            "hidden": 0,
            "invisible": 0,
            "modifiedBy": "R: jalam@redhat.com",
            "productVersionId": 4154741,
            "type": "URL",
            "url": "https://developers.redhat.com/developer-sandbox"
        }

        pid = 4009704
        vid = 4154741

        try:
            response = cgw_client.create_url(pid, vid, data)
        except CGWClientError as e:
            CGWClientError("\nError: %s" % str(e))
            return False
        return response

    def test_delete_url():
        pid = 4009704
        vid = 4154939
        uid = 3871838
        try:
            response = cgw_client.delete_url(pid, vid, uid)
        except CGWClientError as e:
            CGWClientError("\nError: %s" % str(e))
            return False
        return response

    def test_get_internals():
        pid = 4009704
        vid = 4154741
        try:
            response = cgw_client.get_internals(pid, vid)
        except CGWClientError as e:
            CGWClientError("\nError: %s" % str(e))
            return False
        return response

    def test_get_internal():
        pid = 4009704
        vid = 4154741
        uid = 3871838
        try:
            response = cgw_client.get_internal(pid, vid, uid)
        except CGWClientError as e:
            CGWClientError("\nError: %s" % str(e))
            return False
        return response

    def test_create_internal():
        data = {

        }
        pid = 4009704
        vid = 4154741

        try:
            response = cgw_client.create_internal(pid, vid, data)
        except CGWClientError as e:
            CGWClientError("\nError: %s" % str(e))
            return False
        return response

    def test_delete_internal():
        pid = 4009704
        vid = 4154939
        uid = 3871838
        try:
            response = cgw_client.delete_internal(pid, vid, uid)
        except CGWClientError as e:
            CGWClientError("\nError: %s" % str(e))
            return False
        return response

    # Product API Tests
    test_get_product()
    test_get_products()
    test_create_product()
    test_update_product()
    test_delete_product()

    # Version API Tests
    test_get_versions()
    test_get_version()
    test_create_version()
    test_delete_version()

    # Files API Tests
    test_get_all_files()
    test_get_files()
    test_get_file()
    test_create_file()
    test_delete_file()

    # URL API Tests
    test_get_urls()
    test_get_url()
    test_create_url()
    test_delete_url()

    # Internals API Tests
    test_get_internals()
    test_get_internal()
    test_create_internal()
    test_delete_internal()


if __name__ == "__main__":
    test_cgw_client()
