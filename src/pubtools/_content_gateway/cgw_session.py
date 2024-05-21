import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class CGWSession(object):
    """Helper class to support cgw requests and authentication."""

    def __init__(self, hostname, retries=3, verify=True, backoff_factor=2):
        """Initializing.

        Args:
            hostname (str)
                hostname of CG service
            retries (int)
                number of http retries
            verify (bool)
                enable/disable SSL verification
            backoff_factor (int)
                backoff factor to apply between attempts after the second try
        """
        self.session = requests.Session()
        self.hostname = hostname
        self.verify = verify

        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=set(range(500, 512)),
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        self.session.headers["Content-type"] = "application/json"
        self.session.headers["Accept"] = "application/json"

    def get(self, endpoint, **kwargs):
        """HTTP get request against CGW server API

        Args:
            endpoint (str)
                API specific endpoint for the request
        Returns:
            requests.Response
        """

        return self.session.get(self._api_url(endpoint), verify=self.verify, **kwargs)

    def post(self, endpoint, **kwargs):
        """HTTP post request against CGW server API.

        Args:
            endpoint (str)
                API specific endpoint for the request
        Returns:
            requests.Response
        """

        return self.session.post(self._api_url(endpoint), verify=self.verify, **kwargs)

    def put(self, endpoint, **kwargs):
        """HTTP put request against CGW server API.

        Args:
            endpoint (str)
                API specific endpoint for the request
        Returns:
            requests.Response
        """

        return self.session.put(self._api_url(endpoint), verify=self.verify, **kwargs)

    def delete(self, endpoint, **kwargs):
        """HTTP delete request against CGW server API.

        Args:
            endpoint (str)
                API specific endpoint for the request
        Returns:
            requests.Response
        """

        return self.session.delete(self._api_url(endpoint), verify=self.verify, **kwargs)

    def _api_url(self, endpoint):
        """Basic authentication support for CGClient.

        Args:
            endpoint (str)
                API specific endpoint for the request
        Returns:
            requests.Response
        """

        return "%s%s" % (self.hostname, endpoint)
