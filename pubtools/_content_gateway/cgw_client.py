import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from base64 import b64encode


class CGWClient:
    def __init__(self, endpoint, username, password):
        self.endpoint = endpoint.rstrip("/")
        self.username = username
        self.password = password
        self.prefix_url = "/content-gateway/rest/admin"
        self.header = self.get_request_headers()

    def get_request_headers(self):
        if not self.username or not self.password:
            raise CGWClientError("Error: username / password not found !!")

        user_pass_string = "%s:%s" % (self.username, self.password)
        user_pass = b64encode(user_pass_string.encode("utf-8")).decode("ascii")
        headers = {"Authorization": "Basic %s" % user_pass}
        return headers

    def call_cgw_api(self, method, url, params=None, data=None):
        # Ignore the Insecure request warning
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        # Check if CGW endpoint is present
        if not self.endpoint:
            raise CGWClientError("No content gateway endpoint found")

        # Check if Authorization header is present
        if not self.header:
            raise CGWClientError("No authorization header found")

        # Check if correct method id passed
        if method not in ["GET", "POST", "PATCH", "PUT", "DELETE"]:
            raise CGWClientError("Wrong request method passed")

        endpoint_url = "%s%s" % (self.endpoint, url)

        # This print is for debugging purpose only. Will remove it in the final push.
        print(f"URL is {endpoint_url}")
        response = None
        output = True
        try:
            if method == "GET":
                response = requests.get(url=endpoint_url, params=params, verify=False, headers=self.header)
            elif method == "POST":
                response = requests.post(url=endpoint_url, data=data, verify=False, headers=self.header)
            elif method == "PATCH":
                response = requests.patch(url=endpoint_url, data=data, verify=False, headers=self.header)
            elif method == "PUT":
                response = requests.put(url=endpoint_url, data=data, verify=False, headers=self.header)
            elif method == "DELETE":
                response = requests.delete(url=endpoint_url, verify=False, headers=self.header)
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
        url = "%s/products" % self.prefix_url
        resp_data = self.call_cgw_api("GET", url, params=params)
        return resp_data

    def get_product(self, pid, params=None):
        url = "%s/products/%s" % (self.prefix_url, pid)
        resp_data = self.call_cgw_api("GET", url, params=params)
        return resp_data



class CGWClientError(Exception):
    """
    Custom exception to handle Content Gateway Client errors
    """
    def __init__(self, message):
        self.message = message


def unit_test():
    username = ""
    password = ""

    endpoint = "https://content-gateway--stage.apps.ext-waf.mpp.preprod.iad2.dc.paas.redhat.com"
    cgw_client = CGWClient(endpoint, username, password)

    # Get all nodes
    # try:
    #     products = cgw_client.get_products()
    #     print("\nProducts: \n%s" % products)
    # except CGWClientError as e:
    #     return False

    # Get a particular product using node PID
    pid = "400970844"
    try:
        product_details = cgw_client.get_product(pid)
        print("\nProduct Details of PID %s: \n%s" % (pid, product_details))
    except CGWClientError as e:
        return False


if __name__ == "__main__":
    unit_test()
