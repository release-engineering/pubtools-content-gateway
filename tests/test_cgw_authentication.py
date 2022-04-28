from mock import patch, MagicMock, call
from pubtools._content_gateway.cgw_authentication import CGWAuth, CGWBasicAuth
from pubtools._content_gateway.cgw_client import CGWClient


def test_client_auth():
    auth = CGWBasicAuth("foo", "bar")
    cgw = CGWClient("fake-host", auth=auth)
    assert cgw.cg_session.session.headers["auth"] == ("foo", "bar")


def test_cgw_basic_auth():
    session = MagicMock()
    session.session.headers = {}
    auth = CGWBasicAuth("foo", "bar")
    auth.make_auth(session)
    assert session.session.headers["auth"] == ("foo", "bar")


def test_cgwauth_abstract():
    try:
        CGWAuth()
        raise AssertionError("Should raise NotImplementedError")
    except NotImplementedError:
        pass
