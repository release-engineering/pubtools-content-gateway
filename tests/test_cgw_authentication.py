from mock import MagicMock
from pubtools._content_gateway.cgw_authentication import (
    CGWAuth,
    CGWBasicAuth,
    CGWClientError,
)
from pubtools._content_gateway.cgw_client import CGWClient
from base64 import b64encode
import pytest


def test_client_auth():
    auth = CGWBasicAuth("foo", "bar")
    cgw_client = CGWClient("fake-host", cgw_auth=auth)
    user_pass_string = "%s:%s" % ("foo", "bar")
    user_pass = b64encode(user_pass_string.encode("utf-8")).decode("ascii")
    assert cgw_client.cgw_session.session.headers["Authorization"] == "Basic %s" % user_pass


def test_cgw_basic_auth():
    session = MagicMock()
    session.session.headers = {}
    auth = CGWBasicAuth("foo", "bar")
    auth.make_auth(session)

    user_pass_string = "%s:%s" % ("foo", "bar")
    user_pass = b64encode(user_pass_string.encode("utf-8")).decode("ascii")
    assert session.session.headers["Authorization"] == "Basic %s" % user_pass


def test_invalid_cgw_auth():
    session = MagicMock()
    session.session.headers = {}
    auth = CGWBasicAuth("", "")
    with pytest.raises(CGWClientError, match="Error: username / password not found !!"):
        auth.make_auth(session)


def test_cgwauth_abstract():
    try:
        CGWAuth()
        raise AssertionError("Should raise NotImplementedError")
    except NotImplementedError:
        pass
