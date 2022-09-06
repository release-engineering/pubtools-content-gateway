import os
import argparse
import pytest
from pubtools._content_gateway.push_cgw import PushCGW, main
from tests.fake_cgw_client import TestClient

try:
    import mock
except ImportError:
    from unittest import mock

yaml_file_path = os.path.join(os.path.dirname(__file__), "test_data/test_cgw_push.yaml")


@mock.patch("pubtools._content_gateway.push_base.CGWClient", return_value=TestClient())
def test_cgw_operations(mocked_cgw_client):
    push_cgw = PushCGW("http://fake_host_name/test", "foo", "bar", yaml_file_path)
    push_cgw.cgw_operations()

    assert len(push_cgw.cgw_client.create_product.calls) >= 2
    assert len(push_cgw.cgw_client.update_product.calls) >= 1
    assert len(push_cgw.cgw_client.delete_product.calls) >= 1
    assert len(push_cgw.cgw_client.create_version.calls) >= 2
    assert len(push_cgw.cgw_client.update_version.calls) >= 1
    assert len(push_cgw.cgw_client.delete_version.calls) >= 1
    assert len(push_cgw.cgw_client.create_file.calls) >= 1
    assert len(push_cgw.cgw_client.delete_file.calls) >= 1
    assert mocked_cgw_client.called is True


@mock.patch("pubtools._content_gateway.push_cgw.yaml_parser")
@mock.patch("pubtools._content_gateway.push_base.CGWClient", return_value=TestClient())
@mock.patch(
    "pubtools._content_gateway.push_cgw.argparse.ArgumentParser.parse_args",
    return_value=argparse.Namespace(
        CGW_hostname="http://fake_host_nmae/test",
        CGW_username="test_username",
        CGW_password="**********",
        CGW_filepath=yaml_file_path,
    ),
)
def test_main(mock_args, mock_cgw, mock_yaml_parser, create_product_data):
    mock_yaml_parser.return_value = [create_product_data]
    main()
    expected_product_id = 1
    assert expected_product_id in mock_cgw.return_value.products
    assert mock_args.called is True


def test_cgw_operations_exception():
    push_cgw = PushCGW("http://fake_host_name/test", "foo", "bar", yaml_file_path)
    push_cgw.process_product = []
    push_cgw.rollback_cgw_operation = mock.MagicMock()
    with pytest.raises(TypeError):
        push_cgw.cgw_operations()

    assert push_cgw.rollback_cgw_operation.called is True
