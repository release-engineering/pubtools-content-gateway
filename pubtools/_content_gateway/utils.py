import yaml
from yaml.loader import SafeLoader
import jsonschema
from jsonschema import validate
import logging

LOG = logging.getLogger("pubtools.cgw")
LOG_FORMAT = "%(asctime)s [%(levelname)-8s] %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


PRODUCT_SCHEMA = {
    "type": "object",
    "properties": {
        "type": {
            "type": "string"
        },
        "state": {
            "type": "string",
            "enum": ["present", "absent"]
        },
        "metadata": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string"
                },
                "productCode": {
                    "type": ["string", "null"]
                },
                "homepage": {
                    "type": "string"
                },
                "downloadpage": {
                    "type": "string"
                },
                "thankYouPage": {
                    "type": "string"
                },
                "eloquaCode": {
                    "type": ["string", "number"]
                },
                "featuredArtifactType": {
                    "type": "string"
                },
                "thankYouTimeout": {
                    "type": "integer"
                }
            },
            "required": [
                "name",
                "productCode",
                "homepage",
                "downloadpage",
                "thankYouPage",
                "eloquaCode",
                "featuredArtifactType",
                "thankYouTimeout"
            ]
        }
    },
    "required": [
        "type",
        "state",
        "metadata"
    ]
}

VERSION_SCHEMA = {
    "type": "object",
    "properties": {
        "type": {
            "type": "string"
        },
        "state": {
            "type": "string",
            "enum": ["present", "absent"]
        },
        "metadata": {
            "type": "object",
            "properties": {
                "productName": {
                    "type": "string"
                },
                "productCode": {
                    "type": ["string", "null", "number"]
                },
                "versionName": {
                    "type": ["string", "number"]
                },
                "ga": {
                    "type": "boolean"
                },

                "termsAndConditions": {
                    "type": "string"
                },
                "trackingDisabled": {
                    "type": "boolean"
                },
                "hidden": {
                    "type": "boolean"
                },
                "invisible": {
                    "type": "boolean"
                },
                "releaseDate": {
                    "type": "string"
                }
            },
            "required": [
                "productName",
                "productCode",
                "versionName",
                "ga",
                "termsAndConditions",
                "trackingDisabled",
                "hidden",
                "invisible",
                "releaseDate"
            ]
        }
    },
    "required": [
        "type",
        "state",
        "metadata"
    ]
}

FILE_SCHEMA = {
    "type": "object",
    "properties": {
        "type": {
            "type": "string"
        },
        "state": {
            "type": "string",
            "enum": ["present", "absent"]
        },
        "metadata": {
            "type": "object",
            "properties": {
                "productName": {
                    "type": "string"
                },
                "productCode": {
                    "type": ["string", "null"]
                },
                "productVersionName": {
                    "type": ["string", "number", "null"]
                },
                "description": {
                    "type": ["string", "null"]
                },
                "label": {
                    "type": ["string", "null"]
                },
                "order": {
                    "type": "integer"
                },
                "hidden": {
                    "type": "boolean"
                },
                "invisible": {
                    "type": "boolean"
                },
                "type": {
                    "type": "string"
                },
                "differentProductThankYouPage": {
                    "type": ["number", "null"]
                },
                "downloadURL": {
                    "type": "string"
                },
                "shortURL": {
                    "type": "string"
                },
                "size": {
                    "type": ["number", "null"]
                },
                "md5": {
                    "type": ["string", "number", "null"]
                }
            },
            "required": [
                "productName",
                "productCode",
                "productVersionName",
                "description",
                "label",
                "order",
                "hidden",
                "invisible",
                "type",
                "differentProductThankYouPage",
                "downloadURL",
                "shortURL",
                "size",
                "md5"
            ]
        }
    },
    "required": [
        "type",
        "state",
        "metadata"
    ]
}


def validate_data(json_data):
    item_type = json_data.get('type')
    if item_type == 'product':
        validate(instance=json_data, schema=PRODUCT_SCHEMA)
    elif item_type == 'product_version':
        validate(instance=json_data, schema=VERSION_SCHEMA)
    elif item_type == 'file':
        validate(instance=json_data, schema=FILE_SCHEMA)
    LOG.info("Data validation successful for %s: %s" % (item_type, json_data.get('metadata').get('productCode')))
    return True


def yaml_parser(file_path):
    with open(file_path) as f:
        data = list(yaml.load_all(f, Loader=SafeLoader))
    sorted_data = sort_item(data[0])
    return sorted_data


def sort_item(items):
    product_present = []
    version_present = []
    file_present = []
    file_absent = []
    version_absent = []
    product_absent = []
    sorted_items = []

    for data in items:
        validate_data(data)
        if data['type'] == 'product':
            product_present.append(data) if data['state'] == 'present' else product_absent.append(data)

        if data['type'] == 'product_version':
            version_present.append(data) if data['state'] == 'present' else version_absent.append(data)

        if data['type'] == 'file':
            file_present.append(data) if data['state'] == 'present' else file_absent.append(data)

    sorted_items.extend(product_present)
    sorted_items.extend(version_present)
    sorted_items.extend(file_present)
    sorted_items.extend(file_absent)
    sorted_items.extend(version_absent)
    sorted_items.extend(product_absent)

    return sorted_items
