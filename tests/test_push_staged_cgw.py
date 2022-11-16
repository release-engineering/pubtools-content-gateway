from pubtools._content_gateway.push_staged_cgw import PushStagedCGW, entry_point
import pytest
from tests.fake_cgw_client import TestClient
import os
from pushsource import CGWPushItem, FilePushItem
import json

from tests.conftest import test_staging_dir

try:
    import mock
except ImportError:
    from unittest import mock

test_dir = os.path.dirname(__file__)
yaml_file_path = "test_data/test_cgw_push_staged.yaml"
invalid_push_item_path_yaml_file = "test_data/test_invalid_cgw_push_staged.yaml"


@pytest.fixture()
def target_setting():
    return {
        "target_user": "foo",
        "target_password": "bar",
        "target_address": "http://fake/server/",
    }


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
        "md5sum": "test",
        "size": "test",
        "path": "test",
    }

    return Struct(**pulp_push_item)


@mock.patch("pubtools._content_gateway.push_base.CGWClient", return_value=TestClient())
@pytest.mark.parametrize(
    "fixture_source_stage",
    [
        [
            FilePushItem(
                name="dummy-1.0.0-0.x86_64.rpm",
                src="%s/repo1/RPMS/dummy-1.0.0-0.x86_64.rpm" % test_staging_dir(),
                origin="",
            ),
            CGWPushItem(
                name="cgw_push.yaml",
                src="%s/repo1/CGW/cgw.yaml" % test_staging_dir(),
                origin="",
            ),
        ]
    ],
    indirect=True,
)
def test_cgw_operations_success(mocked_cgw_client, target_setting, fixture_source_stage):
    pulp_push_item = get_pulp_push_item()
    push_cgw = PushStagedCGW(["staged:%s" % test_staging_dir()], "fake_target_name", target_setting)
    for item in push_cgw.push_items:
        push_cgw.pulp_push_items[push_cgw.push_item_str(item)] = pulp_push_item
    push_cgw.push_staged_operations()

    assert len(push_cgw.cgw_client.create_product.calls) >= 1
    assert len(push_cgw.cgw_client.create_version.calls) >= 1
    assert len(push_cgw.cgw_client.create_file.calls) >= 1
    assert mocked_cgw_client.called is True


@mock.patch("pubtools._content_gateway.push_base.CGWClient", return_value=TestClient())
@pytest.mark.parametrize(
    "fixture_source_stage",
    [
        [
            FilePushItem(
                name="dummy-1.0.0-0.x86_64.rpm",
                src="%s/repo_invalid/RPMS/dummy-1.0.0-0.x86_64.rpm" % test_staging_dir(),
                origin="",
            ),
            CGWPushItem(
                name="cgw_push.yaml",
                src="%s/repo1/CGW/cgw.yaml" % test_staging_dir(),
                origin="",
            ),
        ]
    ],
    indirect=True,
)
def test_invalid_push_items(mocked_cgw_client, target_setting, fixture_source_stage):
    pulp_push_item = get_pulp_push_item()
    push_cgw = PushStagedCGW(["stage:%s" % test_staging_dir()], "fake_target_name", target_setting)
    for item in push_cgw.push_items:
        push_cgw.pulp_push_items[json.dumps(repr(item), sort_keys=True)] = pulp_push_item

    push_cgw.rollback_cgw_operation = mock.MagicMock()

    with pytest.raises(ValueError) as exception:
        push_cgw.push_staged_operations()

    assert "Unable to find push item with" in str(exception.value)


@mock.patch("pubtools._content_gateway.push_staged_cgw.PushStagedCGW")
def test_entry_point_success(mock_push_cgw, target_setting):
    res = entry_point([], target_setting, "fake_target_name")
    assert res == mock_push_cgw.return_value
    assert mock_push_cgw.call_count == 1
    assert mock_push_cgw.called is True


@pytest.mark.parametrize(
    "fixture_source_stage",
    [
        [
            FilePushItem(
                name="dummy-1.0.0-0.x86_64.rpm",
                src="%s/repo_invalid/RPMS/dummy-1.0.0-0.x86_64.rpm" % test_staging_dir(),
                origin="",
            ),
            CGWPushItem(
                name="cgw_push.yaml",
                src="%s/repo1/CGW/cgw.yaml" % test_staging_dir(),
                origin="",
            ),
        ]
    ],
    indirect=True,
)
def test_pulp_item_push_finished_success(target_setting, fixture_source_stage):
    cgw_item = FilePushItem(
        name="dummy-1.0.0-0.x86_64.rpm",
        src="%s/repo_invalid/RPMS/dummy-1.0.0-0.x86_64.rpm" % test_staging_dir(),
        origin="",
    )

    pulp_push_item = get_pulp_push_item()
    push_cgw = PushStagedCGW(["stage:%s" % test_staging_dir()], "fake_target_name", target_setting)

    push_cgw.pulp_item_push_finished([pulp_push_item], cgw_item)
    assert push_cgw.push_items == [
        FilePushItem(
            name="dummy-1.0.0-0.x86_64.rpm",
            src="%s/repo_invalid/RPMS/dummy-1.0.0-0.x86_64.rpm" % test_staging_dir(),
            origin="",
        ),
        CGWPushItem(
            name="cgw_push.yaml",
            src="%s/repo1/CGW/cgw.yaml" % test_staging_dir(),
            origin="",
        ),
    ]
    assert push_cgw.push_item_str(cgw_item) in push_cgw.pulp_push_items
