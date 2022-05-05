import pytest
import requests_mock
import requests
from pubtools._content_gateway.cgw_client import (
    CGWClient,
    CGWClientError,
)


@pytest.fixture
def fixture_create_product_json():
    json = {
        "name": "Cloud: Virtualization Sandbox testing",
        "eloquaCode": "112233445566"
    }
    return json


@pytest.fixture
def fixture_get_product_json():
    json = {
        "id": 1234567,
        "name": "Cloud: Ansible TEST",
        "homepage": "null",
        "downloadpage": "null",
        "thankYouPage": "null",
        "productCode": "ansibletest",
        "eloquaCode": "NOT_SET",
        "featuredArtifactType": "null",
        "thankYouTimeout": 5,
        "latestURL": "null",
        "created": 1111111111111,
        "updated": 1111111111111,
        "modifiedBy": "R: test@example.com"
    }
    return json


@pytest.fixture
def fixture_get_files_json():
    json = [
        {
            "id": 1234567,
            "description": "Red Hat OpenShift Local",
            "label": "Checksum File",
            "order": 0,
            "created": 1111111111111,
            "updated": 1111111111111,
            "hidden": false,
            "invisible": false,
            "modifiedBy": "R: test@example.com",
            "productVersionId": 1234567,
            "type": "FILE",
            "differentProductThankYouPage": "null",
            "operationSystemPreference": "null",
            "downloadURL": "/test/origin/example/sha256/00/000000000000000000/sha256sum",
            "shortURL": "/test/openshift-v55/example/11.99.44/sha256sum",
            "md5": "null",
            "sha256": "null",
            "size": "null"
        },
        {
            "id": 1234567,
            "description": "Red Hat OpenShift Sandbox",
            "label": "Checksum File Sandbox",
            "order": 0,
            "created": 1111111111111,
            "updated": 1111111111111,
            "hidden": false,
            "invisible": false,
            "modifiedBy": "R: test@example.com",
            "productVersionId": 1234567,
            "type": "FILE",
            "differentProductThankYouPage": "null",
            "operationSystemPreference": "null",
            "downloadURL": "/test/origin/example/sha256/00/000000000000000000/sha256sum",
            "shortURL": "/test/openshift-v55/example/11.99.44/sha256sum",
            "md5": "null",
            "sha256": "null",
            "size": "null"
        }
    ]
    return json


def fixture_get_file_json():
    json = {
        "id": 1234567,
        "description": "Red Hat OpenShift Local",
        "label": "Checksum File",
        "order": 0,
        "created": 1111111111111,
        "updated": 1111111111111,
        "hidden": false,
        "invisible": false,
        "modifiedBy": "R: test@example.com",
        "productVersionId": 1234567,
        "type": "FILE",
        "differentProductThankYouPage": "null",
        "operationSystemPreference": "null",
        "downloadURL": "/test/origin/example/sha256/00/000000000000000000/sha256sum",
        "shortURL": "/test/openshift-v55/example/11.99.44/sha256sum",
        "md5": "null",
        "sha256": "null",
        "size": "null"
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
        fixture_create_product_json,
        fixture_create_version_json,
        fixture_create_file_json,
        fixture_create_url_json,
        fixture_create_internal_json,
):
    with requests_mock.Mocker() as m:
        m.register_uri(
            "PUT",
            "/products",
            status_code=200,
            json=fixture_create_product_json,
        )
        assert requests.put("mock://test.com/products").status_code == 200

        m.register_uri(
            "PUT",
            "/products/versions",
            status_code=200,
            json=fixture_create_version_json,
        )
        assert requests.put("mock://test.com/products/versions").status_code == 200

        m.register_uri(
            "PUT",
            "/products/1/versions/1/files",
            status_code=200,
            json=fixture_create_file_json,
        )
        assert requests.put("mock://test.com/products/1/versions/1/files").status_code == 200

        m.register_uri(
            "PUT",
            "/products/1/versions/1/internal",
            status_code=200,
            json=fixture_create_internal_json,
        )
        assert requests.put("mock://test.com/products/1/versions/1/internal").status_code == 200

        m.register_uri(
            "GET", "/products",
            status_code=200
        )
        assert requests.get("mock://test.com/products").status_code == 200
        m.register_uri(
            "GET",
            "/products/1",
            status_code=200
        )
        assert requests.get("mock://test.com/products/1").status_code == 200
        m.register_uri(
            "DELETE",
            "/products/1",
            status_code=200
        )
        assert requests.delete("mock://test.com/products/1").status_code == 200
        m.register_uri(
            "GET",
            "/products/1/versions",
            status_code=200
        )
        assert requests.get("mock://test.com/products/1/versions").status_code == 200
        m.register_uri(
            "GET",
            "/products/1/versions/1",
            status_code=200
        )
        assert requests.get("mock://test.com/products/1/versions").status_code == 200
        m.register_uri(
            "PUT",
            "/products/1/versions",
            status_code=200
        )
        assert requests.put("mock://test.com/products/1/versions").status_code == 200
        m.register_uri(
            "DELETE",
            "/products/1/versions/1",
            status_code=200
        )
        assert requests.delete("mock://test.com/products/1/versions/1").status_code == 200

        m.register_uri(
            "GET",
            "/products/1/versions/1/urls",
            status_code=200
        )
        assert requests.get("mock://test.com/products/1/versions/1/urls").status_code == 200
        m.register_uri(
            "GET",
            "/products/1/versions/1/urls/1",
            status_code=200
        )
        assert requests.get("mock://test.com/products/1/versions/1/urls/1").status_code == 200
        m.register_uri(
            "PUT",
            "mock://test.com/products/1/versions/1/urls",
            status_code=200,
            json=fixture_create_url_json,
        )
        assert requests.put("mock://test.com/products/1/versions/1/urls").status_code == 200
        m.register_uri(
            "DELETE",
            "/products/1/versions/1/urls/1",
            status_code=200
        )
        assert requests.delete("mock://test.com/products/1/versions/1/urls/1").status_code == 200

        m.register_uri(
            "GET",
            "/products/1/versions/1/files",
            status_code=200
        )
        assert requests.get("mock://test.com/products/1/versions/1/files").status_code == 200

        m.register_uri(
            "GET",
            "/products/1/versions/1/files/1",
            status_code=200
        )
        assert requests.get("mock://test.com/products/1/versions/1/files/1").status_code == 200
        m.register_uri(
            "DELETE",
            "/products/1/versions/1/files/1",
            status_code=200
        )
        assert requests.delete("mock://test.com/products/1/versions/1/files/1").status_code == 200

        m.register_uri(
            "GET",
            "/products/1/versions/1/internals",
            status_code=200
        )
        assert requests.get("mock://test.com/products/1/versions/1/internals").status_code == 200

        m.register_uri(
            "GET",
            "/products/1/versions/1/internals/1",
            status_code=200
        )
        assert requests.get("mock://test.com/products/1/versions/1/internals/1").status_code == 200

        m.register_uri(
            "DELETE",
            "/products/1/versions/1/internals/1",
            status_code=200
        )
        assert requests.delete("mock://test.com/products/1/versions/1/internals/1").status_code == 200


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
