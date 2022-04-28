
# pylint: disable=bad-option-value,useless-object-inheritance
class CGWAuth(object):
    def __init__(self):
        raise NotImplementedError

    def make_auth(self, cg_session):  # pragma: no cover
        raise NotImplementedError


class CGWBasicAuth(CGWAuth):
    """Basic Auth provider to CGWClient."""

    # pylint: disable=super-init-not-called
    def __init__(self, user, password):
        """
        Args:
            user (str)
                Basic auth user name
            password (str)
                Basic auth password
        """
        self.user = user
        self.password = password

    def make_auth(self, cgw_session):
        """Setup IIBSession with basic auth.

        Args:
            cgw_session (IIBSession)
                CGWSession instance
        """

        cgw_session.session.headers["auth"] = (self.user, self.password)
