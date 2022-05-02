from mock import patch, MagicMock, call
from pubtools._content_gateway.cgw_authentication import CGWAuth, CGWBasicAuth
from pubtools._content_gateway.cgw_client import CGWClient


# NOTE: More authentication code to come
def test_client_auth():
    auth = CGWBasicAuth("foo", "bar")
    cgw_client = CGWClient("fake-host", cgw_auth=auth)


def test_cgw_basic_auth():
    session = MagicMock()
    session.session.headers = {}
    auth = CGWBasicAuth("foo", "bar")
    auth.make_auth(session)


def test_cgwauth_abstract():
    try:
        CGWAuth()
        raise AssertionError("Should raise NotImplementedError")
    except NotImplementedError:
        pass
