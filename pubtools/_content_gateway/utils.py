import yaml
from yaml.loader import SafeLoader
from jsonschema import validate
import logging

LOG = logging.getLogger("pubtools.cgw")
LOG_FORMAT = "%(asctime)s [%(levelname)-8s] %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

PRODUCT_SCHEMA = {
    "type": "object",
    "properties": {
        "type": {"type": "string"},
        "state": {"type": "string", "enum": ["create", "update", "delete"]},
        "metadata": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "productCode": {"type": ["string", "null"]},
                "homepage": {"type": "string"},
                "downloadpage": {"type": "string"},
                "thankYouPage": {"type": "string"},
                "eloquaCode": {"type": ["string", "number"]},
                "featuredArtifactType": {"type": "string"},
                "thankYouTimeout": {"type": "integer"},
            },
            "required": [
                "name",
                "productCode",
                "homepage",
                "downloadpage",
                "thankYouPage",
                "eloquaCode",
                "featuredArtifactType",
                "thankYouTimeout",
            ],
        },
    },
    "required": ["type", "state", "metadata"],
}

VERSION_SCHEMA = {
    "type": "object",
    "properties": {
        "type": {"type": "string"},
        "state": {"type": "string", "enum": ["create", "update", "delete"]},
        "metadata": {
            "type": "object",
            "properties": {
                "productName": {"type": "string"},
                "productCode": {"type": ["string", "null", "number"]},
                "versionName": {"type": ["string", "number"]},
                "ga": {"type": "boolean"},
                "termsAndConditions": {"type": "string"},
                "trackingDisabled": {"type": "boolean"},
                "hidden": {"type": "boolean"},
                "invisible": {"type": "boolean"},
                "releaseDate": {"type": "string"},
            },
            "required": [
                "productName",
                "productCode",
                "versionName",
                "ga",
                "termsAndConditions",
                "trackingDisabled",
                "hidden",
                "releaseDate",
            ],
        },
    },
    "required": ["type", "state", "metadata"],
}

FILE_SCHEMA = {
    "type": "object",
    "properties": {
        "type": {"type": "string"},
        "state": {"type": "string", "enum": ["create", "update", "delete"]},
        "metadata": {
            "type": "object",
            "properties": {
                "productName": {"type": "string"},
                "productCode": {"type": ["string", "null"]},
                "productVersionName": {"type": ["string", "number", "null"]},
                "description": {"type": ["string", "null"]},
                "label": {"type": ["string", "null"]},
                "order": {"type": "integer"},
                "hidden": {"type": "boolean"},
                "invisible": {"type": "boolean"},
                "type": {"type": "string"},
                "differentProductThankYouPage": {"type": ["number", "null"]},
                "downloadURL": {"type": "string"},
                "shortURL": {"type": "string"},
                "size": {"type": ["number", "null"]},
                "md5": {"type": ["string", "number", "null"]},
            },
            "required": [
                "productName",
                "productCode",
                "productVersionName",
                "description",
                "label",
                "order",
                "hidden",
                "type",
                "differentProductThankYouPage",
                "downloadURL",
                "shortURL",
                "size",
                "md5",
            ],
        },
    },
    "required": ["type", "state", "metadata"],
}

FILE_STAGED_SCHEMA = {
    "type": "object",
    "properties": {
        "type": {"type": "string"},
        "state": {"type": "string", "enum": ["create", "update", "delete"]},
        "metadata": {
            "type": "object",
            "properties": {
                "productName": {"type": "string"},
                "productCode": {"type": ["string", "null"]},
                "productVersionName": {"type": ["string", "number", "null"]},
                "description": {"type": ["string", "null"]},
                "label": {"type": ["string", "null"]},
                "order": {"type": "integer"},
                "hidden": {"type": "boolean"},
                "invisible": {"type": "boolean"},
                "type": {"type": "string"},
                "differentProductThankYouPage": {"type": ["number", "null"]},
                "shortURL": {"type": "string"},
                "pushItemPath": {"type": "string"},
            },
            "required": [
                "productName",
                "productCode",
                "productVersionName",
                "description",
                "label",
                "order",
                "hidden",
                "type",
                "differentProductThankYouPage",
                "shortURL",
                "pushItemPath",
            ],
        },
    },
    "required": ["type", "state", "metadata"],
}


def validate_data(json_data, staged=False):
    """
    Validate that json_data contains all the necessary data
    with defined with json schemas

    Args:
        json_data (dict)
            JSON dictionary with content gateway data
        staged (bool)
            optional. Indicates if resulting json_data needs to
            validate against FILE_STAGED_SCHEMA

    Raises:
        ValidationError
            The json_data type doesn't match with schema
    Returns:
        True: if validation succeed
    """

    item_type = json_data.get("type")
    if item_type == "product":
        validate(instance=json_data, schema=PRODUCT_SCHEMA)
    elif item_type == "product_version":
        validate(instance=json_data, schema=VERSION_SCHEMA)
    elif item_type == "file":
        validate(instance=json_data, schema=FILE_STAGED_SCHEMA if staged else FILE_SCHEMA)
    LOG.info("Data validation successful for %s: %s" % (item_type, json_data.get("metadata").get("productCode")))
    return True


def yaml_parser(file_path):
    """
    Parse the yaml data into json data

    Args:
        file_path (str)
            JSON dictionary with content gateway data
    Raises:
        FileNotFoundError
            If the file_path cannot be found
    Returns:
        list(dict): parsed json data from yaml file
    """

    with open(file_path) as f:
        data = list(yaml.load_all(f, Loader=SafeLoader))
    return data[0]


def sort_items(items):
    """
    Sort the items in the following order
        1) all products with state present
        2) all versions with state present
        3) all files with state present
        4) all files with state absent
        5) all versions with state absent
        6) all products with state absent

    This is needed to process all the present state of products,
    versions and files first then absent state of files, versions and products

    This sorting is needed for the following reasons:
        1) A file cannot be created if it's parent version and product are not present.
            All parent data need to be present before creating child object.
        2) A product cannot get deleted if it has versions and file.
            All nested data need to be cleared before deleting parent object

    Args:
        items (list(dict))
            list of JSON dictionary
    Returns:
        list(dict): list of JSON dictionary
    """
    product_create_update = []
    version_create_update = []
    file_create_update = []
    file_delete = []
    version_delete = []
    product_delete = []
    sorted_items = []

    for data in items:
        if data["type"] == "product":
            product_create_update.append(data) if data["state"] in ["create", "update"] else product_delete.append(data)

        if data["type"] == "product_version":
            version_create_update.append(data) if data["state"] in ["create", "update"] else version_delete.append(data)

        if data["type"] == "file":
            file_create_update.append(data) if data["state"] in ["create", "update"] else file_delete.append(data)

    sorted_items.extend(product_create_update)
    sorted_items.extend(version_create_update)
    sorted_items.extend(file_create_update)
    sorted_items.extend(file_delete)
    sorted_items.extend(version_delete)
    sorted_items.extend(product_delete)

    return sorted_items
