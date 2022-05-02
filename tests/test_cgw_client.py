import pytest
import requests_mock
import requests
from requests import HTTPError

from pubtools._content_gateway.cgw_client import (
    CGWClient,
    CGWClientError,
)

# NOTE: More test code to come
@pytest.fixture
def fixture_create_product_json():
    json = {
            "name": "Cloud: Virtualization Sandbox testing",
            "eloquaCode": "112233445566"
        }
    return json

@pytest.fixture
def fixture_create_version_json():
    json = {
            "productId": 123456,
            "versionName": "v1",
            "termsAndConditions": "Basic user account"
        }
    return json


@pytest.fixture
def fixture_create_file_json():
    json = {
            "description": "Test Local Sandbox",
            "label": "Checksum File Sandbox",
            "order": 0,
            "hidden": 0,
            "invisible": 0,
            "modifiedBy": "R: test@example.com",
            "productVersionId": 123456,
            "type": "FILE",
            "downloadURL": "https://www.example.com/",
            "shortURL": "https://www.example.com/"
        }
    return json


@pytest.fixture
def fixture_create_url_json():
    json = {
            "description": "Sandbox URL",
            "label": "Sandbox URL Testing",
            "hidden": 0,
            "invisible": 0,
            "modifiedBy": "R: test@example.com",
            "productVersionId": 1234567,
            "type": "URL",
            "url": "https://www.example.com/"
        }
    return json


@pytest.fixture
def fixture_create_internal_json():
    json = {

    }
    return json


def test_cgw_client(
    fixture_create_version_json,
    fixture_create_file_json,
    fixture_create_url_json,
    fixture_create_internal_json,
):
    with requests_mock.Mocker() as m:
        m.register_uri(
            "PUT",
            "/products/",
            status_code=200,
            json=fixture_create_product_json,
        )
        m.register_uri(
            "PUT",
            "/products/versions",
            status_code=200,
            json=fixture_create_version_json,
        )

        m.register_uri(
            "PUT",
            "/products/1/versions/1/files",
            status_code=200,
            json=fixture_create_file_json,
        )

        m.register_uri(
            "PUT",
            "/products/1/versions/1/internal",
            status_code=200,
            json=fixture_create_internal_json,
        )

        m.register_uri(
            "GET", "/products",
            status_code=200
        )
        m.register_uri(
            "GET",
            "/products/1",
            status_code=200
        )
        m.register_uri(
            "DELETE",
            "/products/1",
            status_code=200
        )
        m.register_uri(
            "GET",
            "/products/1/versions",
            status_code=200
        )
        m.register_uri(
            "GET",
            "/products/1/versions/1",
            status_code=200
        )
        m.register_uri(
            "PUT",
            "/products/1/versions",
            status_code=200
        )
        m.register_uri(
            "DELETE",
            "/products/1/versions/1",
            status_code=200
        )

        m.register_uri(
            "GET",
            "/products/1/versions/1/urls",
            status_code=200
        )
        m.register_uri(
            "GET",
            "/products/1/versions/1/urls/1",
            status_code=200
        )
        m.register_uri(
            "PUT",
            "/products/1/versions/1/urls",
            status_code=200,
            json=fixture_create_url_json,
        )
        m.register_uri(
            "DELETE",
            "/products/1/versions/1/urls/1",
            status_code=200
        )

        m.register_uri(
            "GET",
            "/products/1/versions/1/files",
            status_code=200
        )
        m.register_uri(
            "GET",
            "/products/1/versions/1/files/1",
            status_code=200
        )
        m.register_uri(
            "DELETE",
            "/products/1/versions/1/files/1",
            status_code=200
        )

        m.register_uri(
            "GET",
            "/products/1/versions/1/internals",
            status_code=200
        )
        m.register_uri(
            "GET",
            "/products/1/versions/1/internals/1",
            status_code=200
        )
        m.register_uri(
            "DELETE",
            "/products/1/versions/1/internals/1",
            status_code=200
        )


def test_cgw_error_response():
    with requests_mock.Mocker() as m:
        m.register_uri(
            "GET",
            "/products",
            status_code=400,
            json={"error": "An ugly error has occurred!"},
        )

        cgwc = CGWClient("fake-host")
        with pytest.raises(CGWClientError):
            cgwc.get_products()
