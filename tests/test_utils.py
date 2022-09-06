import os
from pubtools._content_gateway.utils import yaml_parser, validate_data, sort_items
import pytest

test_data_dir = os.path.join(os.path.dirname(__file__), "test_data")


def test_validate_data(fixture_sorted_files_json):
    for data in fixture_sorted_files_json:
        assert validate_data(data) is True


def test_yaml_parser():
    yaml_file = os.path.join(test_data_dir, "test_cgw_push.yaml")
    yaml_parser(yaml_file)


def test_yaml_file_not_found_exception():
    yaml_file = os.path.join(test_data_dir, "invalid_cgw_push.yaml")
    with pytest.raises(FileNotFoundError) as exp:
        yaml_parser(yaml_file)
    assert str(exp.value) == "[Errno 2] No such file or directory: '%s'" % yaml_file


def test_sort_items(fixture_unsorted_files_json, fixture_sorted_files_json):
    assert fixture_sorted_files_json == sort_items(fixture_unsorted_files_json)
