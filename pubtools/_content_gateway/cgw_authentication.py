from base64 import b64encode


class CGWAuth(object):
    """Custom exception to handle authentication errors."""

    def __init__(self):
        raise NotImplementedError

    def make_auth(self, cgw_session):
        raise NotImplementedError  # pragma: no cover


class CGWClientError(Exception):
    """Custom exception to handle Content Gateway Client errors."""

    def __init__(self, message):
        self.message = message


class CGWBasicAuth(CGWAuth):
    """Basic Auth provider to CGWClient."""

    # pylint: disable=super-init-not-called
    def __init__(self, user, password):
        """Initializing

        Args:
            user (str)
                Basic auth user_name
            password (str)
                Basic auth password
        """
        self.user = user
        self.password = password

    def make_auth(self, cgw_session=None):
        """Setup CGWSession with basic auth.

        Args:
            cgw_session (CGWSession)
                CGWSession instance
        """

        if not self.user or not self.password:
            raise CGWClientError("Error: username / password not found !!")

        user_pass_string = "%s:%s" % (self.user, self.password)
        user_pass = b64encode(user_pass_string.encode("utf-8")).decode("ascii")
        cgw_session.session.headers["Authorization"] = "Basic %s" % user_pass
