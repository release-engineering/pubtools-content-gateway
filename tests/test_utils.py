import os
from pubtools._content_gateway.utils import yaml_parser, validate_data, sort_items, format_cgw_items

test_data_dir = os.path.join(os.path.dirname(__file__), "test_data")


def test_validate_data(fixture_sorted_files_json):
    for data in fixture_sorted_files_json:
        assert validate_data(data) is True


def test_yaml_parser():
    yaml_file = os.path.join(test_data_dir, "test_cgw_push.yaml")
    yaml_parser(yaml_file)


def test_sort_items(fixture_unsorted_files_json, fixture_sorted_files_json):
    assert fixture_sorted_files_json == sort_items(fixture_unsorted_files_json)


def test_yml_data_formats(yml_json_data):
    yaml_file = os.path.join(test_data_dir, "test_yml_format.yaml")
    cgw_items = yaml_parser(yaml_file)
    formatted_cgw_data = format_cgw_items(cgw_items)
    assert formatted_cgw_data == yml_json_data
