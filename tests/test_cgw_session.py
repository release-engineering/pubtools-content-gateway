try:
    from unittest.mock import patch
except ImportError:
    from mock import patch
from pubtools._content_gateway.cgw_session import CGWSession


@patch("requests.Session.get")
@patch("requests.Session.post")
@patch("requests.Session.put")
@patch("requests.Session.delete")
def test_cgw_session_methods(patched_delete, patched_put, patched_post, patched_get):
    cgw_session = CGWSession("https://fake-host")
    cgw_session.get("/fake-end-point")
    cgw_session.post("/fake-end-point")
    cgw_session.put("/fake-end-point")
    cgw_session.delete("/fake-end-point")

    patched_get.assert_called_with("https://fake-host/fake-end-point", verify=True)
    patched_post.assert_called_with("https://fake-host/fake-end-point", verify=True)
    patched_put.assert_called_with("https://fake-host/fake-end-point", verify=True)
    patched_delete.assert_called_with("https://fake-host/fake-end-point", verify=True)
