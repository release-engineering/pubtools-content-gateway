from mock import patch

from pubtools._content_gateway.cgw_session import CGWSession



@patch("requests.Session.get")
@patch("requests.Session.post")
@patch("requests.Session.put")
@patch("requests.Session.delete")
def test_cgw_session_methods(patched_delete, patched_put, patched_post, patched_get):
    cg_session = CGWSession("fake-host")
    cg_session.get("fake-end-point")
    cg_session.post("fake-end-point")
    cg_session.put("fake-end-point")
    cg_session.delete("fake-end-point")

    patched_get.assert_called_with(
        "https://fake-host/api/v1/fake-end-point", verify=True
    )
    patched_post.assert_called_with(
        "https://fake-host/api/v1/fake-end-point", verify=True
    )
    patched_put.assert_called_with(
        "https://fake-host/api/v1/fake-end-point", verify=True
    )
    patched_delete.assert_called_with(
        "https://fake-host/api/v1/fake-end-point", verify=True
    )
