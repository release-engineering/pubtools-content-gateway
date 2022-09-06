from pubtools._content_gateway.push_staged_cgw import PushStagedCGW, entry_point
import pytest
from tests.fake_cgw_client import TestClient
import os
from pushsource import CGWPushItem, FilePushItem
import json
from attrs import asdict

try:
    import mock
except ImportError:
    from unittest import mock

test_dir = os.path.dirname(__file__)
yaml_file_path = "test_data/test_cgw_push_staged.yaml"
invalid_push_item_path_yaml_file = "test_data/test_invalid_cgw_push_staged.yaml"


@pytest.fixture()
def target_setting():
    return {"username": "foo", "password": "bar", "server_name": "http://fake/server/"}


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


def get_pulp_push_item():
    pulp_push_item = {
        "repository_memberships": "test",
        "content_type_id": "test",
        "cdn_published": "test",
        "cdn_path": "test",
        "display_order": "test",
        "version": "v1",
        "description": "test",
        "sha256sum": "test",
        "size": "test",
        "path": "test",
    }

    return Struct(**pulp_push_item)


@mock.patch("pubtools._content_gateway.push_base.CGWClient", return_value=TestClient())
def test_cgw_operations_success(mocked_cgw_client, target_setting):
    cgw_item = CGWPushItem(name="cgw_push.yaml", src=yaml_file_path, origin=test_dir)
    file_item = FilePushItem(name="file_push.yaml", src=yaml_file_path, origin=test_dir)

    pulp_push_item = get_pulp_push_item()
    push_cgw = PushStagedCGW("fake_target_name", target_setting)
    push_cgw.push_items = [file_item, cgw_item]
    for item in push_cgw.push_items:
        push_cgw.pulp_push_items[json.dumps(asdict(item), sort_keys=True)] = pulp_push_item
    push_cgw.push_staged_operations()

    assert len(push_cgw.cgw_client.create_product.calls) >= 1
    assert len(push_cgw.cgw_client.create_version.calls) >= 1
    assert len(push_cgw.cgw_client.create_file.calls) >= 1
    assert mocked_cgw_client.called is True


def test_invalid_push_items(target_setting):
    cgw_item = CGWPushItem(name="cgw_push.yaml", src=invalid_push_item_path_yaml_file, origin=test_dir)
    file_item = FilePushItem(name="file_push.yaml", src=invalid_push_item_path_yaml_file, origin=test_dir)

    pulp_push_item = get_pulp_push_item()
    push_cgw = PushStagedCGW("fake_target_name", target_setting)
    push_cgw.push_items = [file_item, cgw_item]
    for item in push_cgw.push_items:
        push_cgw.pulp_push_items[json.dumps(asdict(item), sort_keys=True)] = pulp_push_item

    push_cgw.rollback_cgw_operation = mock.MagicMock()

    with pytest.raises(ValueError) as exception:
        push_cgw.push_staged_operations()

    assert "Unable to find push item with" in str(exception.value)


def test_invalid_file_path(target_setting):
    cgw_item = CGWPushItem(name="cgw_push.yaml", src="invalid_push_item_file_path", origin=test_dir)
    file_item = FilePushItem(name="file_push.yaml", src="invalid_push_item_file_path", origin=test_dir)

    pulp_push_item = get_pulp_push_item()
    push_cgw = PushStagedCGW("fake_target_name", target_setting)
    push_cgw.push_items = [file_item, cgw_item]
    for item in push_cgw.push_items:
        push_cgw.pulp_push_items[json.dumps(asdict(item), sort_keys=True)] = pulp_push_item

    with pytest.raises(FileNotFoundError) as exception:
        push_cgw.push_staged_operations()
    assert "No such file or directory" in str(exception.value)


@mock.patch("pubtools._content_gateway.push_staged_cgw.PushStagedCGW", return_value="test")
def test_entry_point_success(mock_push_cgw, target_setting):
    res = entry_point(target_setting, "fake_target_name")
    expected_result = "test"
    assert res == expected_result
    assert mock_push_cgw.call_count == 1
    assert mock_push_cgw.called is True


def test_gather_source_items_success(target_setting):
    cgw_item = CGWPushItem(name="cgw_push.yaml", src="invalid_push_item_file_path", origin=test_dir)

    pulp_push_item = get_pulp_push_item()
    push_cgw = PushStagedCGW("fake_target_name", target_setting)

    push_cgw.gather_source_items(pulp_push_item, cgw_item)
    assert push_cgw.push_items == [cgw_item]
    assert json.dumps(asdict(cgw_item), sort_keys=True) in push_cgw.pulp_push_items


def test_cgw_operations_exception(target_setting):
    cgw_item = CGWPushItem(name="cgw_push.yaml", src=yaml_file_path, origin=test_dir)

    pulp_push_item = get_pulp_push_item()
    push_cgw = PushStagedCGW("fake_target_name", target_setting)
    push_cgw.gather_source_items(pulp_push_item, cgw_item)
    push_cgw.process_product = []
    push_cgw.rollback_cgw_operation = mock.MagicMock()

    with pytest.raises(TypeError):
        push_cgw.push_staged_operations()
    assert push_cgw.rollback_cgw_operation.called is True
