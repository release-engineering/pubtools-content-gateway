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


def validate_schema(json_data):
    try:
        if json_data.get('type') == 'product':
            validate(instance=json_data, schema=PRODUCT_SCHEMA)
        elif json_data.get('type') == 'product_version':
            validate(instance=json_data, schema=VERSION_SCHEMA)
        elif json_data.get('type') == 'file':
            validate(instance=json_data, schema=FILE_SCHEMA)
    except jsonschema.exceptions.ValidationError as error:
        LOG.exception(error)
        return False
    return True


def yaml_parser(file_path):
    try:
        with open(file_path) as f:
            data = list(yaml.load_all(f, Loader=SafeLoader))
        return data[0]
    except Exception as error:
        LOG.exception(error)
