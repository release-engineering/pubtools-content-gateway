import pytest
import requests_mock
from pubtools._content_gateway.cgw_client import (
    CGWClient,
    CGWClientError,
)
from pubtools._content_gateway.cgw_authentication import CGWBasicAuth


@pytest.fixture
def get_all_products_response_json():
    json = [
        {
            "id": 111111,
            "name": "Cloud: Ansible Test",
            "productCode": "AnsibleTest",
            "latestURL": "null",
            "created": 1111111111111,
            "updated": 1111111111111,
            "modifiedBy": "R: test@example.com",
            "homepage": "https://test.fixture.com/",
            "downloadpage": "https://test.fixture.com/",
            "thankYouPage": "https://test.fixture.com/",
            "eloquaCode": "NOT_SET",
            "featuredArtifactType": "Server",
            "thankYouTimeout": 5,
        },
        {
            "id": 222222,
            "name": "Openstack: Server Test",
            "productCode": "OpenstackServerTest",
            "latestURL": "null",
            "created": 22222222,
            "updated": 22222222,
            "modifiedBy": "R: test@example.com",
            "homepage": "https://test.fixture.com/",
            "downloadpage": "https://test.fixture.com/",
            "thankYouPage": "https://test.fixture.com/",
            "eloquaCode": "NOT_SET",
            "featuredArtifactType": "Server",
            "thankYouTimeout": 5,
        },
    ]
    return json


@pytest.fixture
def product_response_json():
    json = {
        "id": 111111,
        "name": "Cloud: Ansible NEW Test",
        "productCode": "AnsibleNewTest",
        "latestURL": "null",
        "created": 1111111111111,
        "updated": 1111111111111,
        "modifiedBy": "R: test@example.com",
        "homepage": "https://test.fixture.com/",
        "downloadpage": "https://test.fixture.com/",
        "thankYouPage": "https://test.fixture.com/",
        "eloquaCode": "NOT_SET",
        "featuredArtifactType": "Server",
        "thankYouTimeout": 5,
    }
    return json


@pytest.fixture
def get_all_versions_response_json():
    json = [
        {
            "id": 333333,
            "productId": 111111,
            "versionName": "v1",
            "ga": False,
            "created": 1619209855705,
            "updated": 1619209855705,
            "modifiedBy": "R: jalam",
            "masterProductVersion": None,
            "termsAndConditions": "Anonymous Download",
            "trackingDisabled": False,
            "hidden": False,
            "invisible": False,
            "releaseDate": 1619136000000,
        },
        {
            "id": 444444,
            "productId": 111111,
            "versionName": "v2",
            "ga": False,
            "created": 1619209855705,
            "updated": 1619209855705,
            "modifiedBy": "R: jalam",
            "masterProductVersion": None,
            "termsAndConditions": "Anonymous Download",
            "trackingDisabled": False,
            "hidden": False,
            "invisible": False,
            "releaseDate": 1619136000000,
        },
    ]
    return json


@pytest.fixture
def version_response_json():
    json = {
        "id": 333333,
        "productId": 111111,
        "versionName": "v1",
        "ga": False,
        "created": 1619209855705,
        "updated": 1619209855705,
        "modifiedBy": "R: jalam",
        "masterProductVersion": None,
        "termsAndConditions": "Anonymous Download",
        "trackingDisabled": False,
        "hidden": False,
        "invisible": False,
        "releaseDate": 1619136000000,
    }
    return json


@pytest.fixture
def get_all_files_response_json():
    json = [
        {
            "id": 111111,
            "description": "Red Hat OpenShift Local",
            "label": "Checksum File",
            "order": 0,
            "created": 1111111111111,
            "updated": 1111111111111,
            "hidden": False,
            "invisible": False,
            "modifiedBy": "R: test@example.com",
            "productVersionId": 111111,
            "type": "FILE",
            "differentProductThankYouPage": None,
            "operationSystemPreference": None,
            "downloadURL": "/test/fake/openshift/downloadURL/1",
            "shortURL": "/test/fake/openshift/shortURL",
            "md5": "null",
            "sha256": None,
            "size": None,
        },
        {
            "id": 222222,
            "description": "Red Hat OpenShift Sandbox",
            "label": "Checksum File Sandbox",
            "order": 0,
            "created": 1111111111111,
            "updated": 1111111111111,
            "hidden": False,
            "invisible": False,
            "modifiedBy": "R: test@example.com",
            "productVersionId": 111111,
            "type": "FILE",
            "differentProductThankYouPage": None,
            "operationSystemPreference": None,
            "downloadURL": "/test/fake/openshift/downloadURL/2",
            "shortURL": "/test/fake/openshift/shortURL",
            "md5": "null",
            "sha256": "null",
            "size": "null",
        },
    ]
    return json


@pytest.fixture
def file_response_json():
    json = {
        "id": 111111,
        "description": "Red Hat OpenShift Local",
        "label": "Checksum File",
        "order": 0,
        "created": 1111111111111,
        "updated": 1111111111111,
        "hidden": False,
        "invisible": False,
        "modifiedBy": "R: test@example.com",
        "productVersionId": 111111,
        "type": "FILE",
        "differentProductThankYouPage": None,
        "operationSystemPreference": None,
        "downloadURL": "/test/fake/openshift/downloadURL/1",
        "shortURL": "/test/fake/openshift/shortURL",
        "md5": "null",
        "sha256": None,
        "size": None,
    }
    return json


@pytest.fixture()
def cgw_client():
    auth = CGWBasicAuth("foo", "bar")
    return CGWClient("mock://test.com/", auth)


def test_get_products_success(get_all_products_response_json, cgw_client):
    with requests_mock.Mocker() as m:
        m.register_uri(
            "GET",
            "mock://test.com/products",
            status_code=200,
            json=get_all_products_response_json,
        )
        response = cgw_client.get_products()
        assert m.call_count == 1
        assert get_all_products_response_json == response


def test_get_products_failed(cgw_client):
    with requests_mock.Mocker() as m:
        m.register_uri(
            "GET",
            "mock://test.com/products",
            status_code=404,
            json=False,
        )
        with pytest.raises(
            CGWClientError,
            match="content gateway API returned error: " "\nstatus_code: 404, " "reason: None, " "error: false",
        ):
            cgw_client.get_products()
        assert m.call_count == 1


def test_get_single_product_success(product_response_json, cgw_client):
    with requests_mock.Mocker() as m:
        m.register_uri(
            "GET",
            "mock://test.com/products/1",
            status_code=200,
            json=product_response_json,
        )
        response = cgw_client.get_product(1)
        assert m.call_count == 1
        assert product_response_json == response


def test_create_product_success(create_product_data, product_response_json, cgw_client):
    with requests_mock.Mocker() as m:
        m.register_uri(
            "PUT",
            "mock://test.com/products/",
            status_code=200,
            json=product_response_json,
        )
        response = cgw_client.create_product(create_product_data["metadata"])
        assert m.call_count == 1
        assert product_response_json == response


def test_update_product_success(update_product_data, product_response_json, cgw_client):
    with requests_mock.Mocker() as m:
        m.register_uri(
            "POST",
            "mock://test.com/products",
            status_code=200,
            json=product_response_json,
        )
        response = cgw_client.update_product(update_product_data["metadata"])
        assert m.call_count == 1
        assert product_response_json == response


def test_delete_product_success(cgw_client):
    with requests_mock.Mocker() as m:
        m.register_uri(
            "DELETE",
            "mock://test.com/products/1",
            status_code=200,
        )
        cgw_client.delete_product(1)
        assert m.call_count == 1


def test_get_versions_success(get_all_versions_response_json, cgw_client):
    with requests_mock.Mocker() as m:
        m.register_uri(
            "GET",
            "mock://test.com/products/1/versions",
            status_code=200,
            json=get_all_versions_response_json,
        )
        response = cgw_client.get_versions(1)
        assert m.call_count == 1
        assert get_all_versions_response_json == response


def test_get_version_failed(cgw_client):
    with requests_mock.Mocker() as m:
        m.register_uri(
            "GET",
            "mock://test.com/products/1/versions",
            status_code=404,
            json=False,
        )
        with pytest.raises(
            CGWClientError,
            match="content gateway API returned error: " "\nstatus_code: 404, " "reason: None, " "error: false",
        ):
            cgw_client.get_versions(1)
        assert m.call_count == 1


def test_get_single_version_success(version_response_json, cgw_client):
    with requests_mock.Mocker() as m:
        m.register_uri(
            "GET",
            "mock://test.com/products/1/versions/1",
            status_code=200,
            json=version_response_json,
        )
        response = cgw_client.get_version(1, 1)
        assert m.call_count == 1
        assert version_response_json == response


def test_create_version_success(version_response_json, create_version_data, cgw_client):
    with requests_mock.Mocker() as m:
        m.register_uri(
            "PUT",
            "mock://test.com/products/1/versions/",
            status_code=200,
            json=version_response_json,
        )
        response = cgw_client.create_version(1, create_version_data["metadata"])
        assert m.call_count == 1
        assert version_response_json == response


def test_update_version_success(version_response_json, create_version_data, cgw_client):
    with requests_mock.Mocker() as m:
        m.register_uri(
            "POST",
            "mock://test.com/products/1/versions",
            status_code=200,
            json=version_response_json,
        )
        response = cgw_client.update_version(1, create_version_data["metadata"])
        assert m.call_count == 1
        assert version_response_json == response


def test_delete_version_success(cgw_client):
    with requests_mock.Mocker() as m:
        m.register_uri(
            "DELETE",
            "mock://test.com/products/1/versions/1",
            status_code=200,
        )
        cgw_client.delete_version(1, 1)
        assert m.call_count == 1


def test_get_files_success(get_all_files_response_json, cgw_client):
    with requests_mock.Mocker() as m:
        m.register_uri(
            "GET",
            "mock://test.com/products/1/versions/1/files",
            status_code=200,
            json=get_all_files_response_json,
        )
        response = cgw_client.get_files(1, 1)
        assert m.call_count == 1
        assert get_all_files_response_json == response


def test_get_all_files_success(get_all_files_response_json, cgw_client):
    with requests_mock.Mocker() as m:
        m.register_uri(
            "GET",
            "mock://test.com/products/1/versions/1/all",
            status_code=200,
            json=get_all_files_response_json,
        )
        response = cgw_client.get_all_files(1, 1)
        assert m.call_count == 1
        assert get_all_files_response_json == response


def test_get_files_failed(cgw_client):
    with requests_mock.Mocker() as m:
        m.register_uri(
            "GET",
            "mock://test.com/products/1/versions/1/files/1",
            status_code=404,
            json=False,
        )
        with pytest.raises(
            CGWClientError,
            match="content gateway API returned error: " "\nstatus_code: 404, " "reason: None, " "error: false",
        ):
            cgw_client.get_file(1, 1, 1)
        assert m.call_count == 1


def test_get_single_file_success(file_response_json, cgw_client):
    with requests_mock.Mocker() as m:
        m.register_uri(
            "GET",
            "mock://test.com/products/1/versions/1/files/1",
            status_code=200,
            json=file_response_json,
        )
        response = cgw_client.get_file(1, 1, 1)
        assert m.call_count == 1
        assert file_response_json == response


def test_create_file_success(file_response_json, create_file_data, cgw_client):
    with requests_mock.Mocker() as m:
        m.register_uri(
            "PUT",
            "mock://test.com/products/1/versions/1/files",
            status_code=200,
            json=file_response_json,
        )
        response = cgw_client.create_file(1, 1, create_file_data["metadata"])
        assert m.call_count == 1
        assert file_response_json == response


def test_update_file_success(file_response_json, create_version_data, cgw_client):
    with requests_mock.Mocker() as m:
        m.register_uri(
            "POST",
            "mock://test.com/products/1/versions/1/files",
            status_code=200,
            json=file_response_json,
        )
        response = cgw_client.update_file(1, 1, create_version_data["metadata"])
        assert m.call_count == 1
        assert file_response_json == response


def test_delete_file_success(cgw_client):
    with requests_mock.Mocker() as m:
        m.register_uri(
            "DELETE",
            "mock://test.com/products/1/versions/1/files/1",
            status_code=200,
        )
        cgw_client.delete_file(1, 1, 1)
        assert m.call_count == 1


def test_get_urls_success(cgw_client):
    test_url = {"url": "test/url"}
    with requests_mock.Mocker() as m:
        m.register_uri(
            "GET",
            "mock://test.com/products/1/versions/1/urls",
            status_code=200,
            json=test_url,
        )
        response = cgw_client.get_urls(1, 1)
        assert m.call_count == 1
        assert response == test_url


def test_get_urls_failed(cgw_client):
    with requests_mock.Mocker() as m:
        m.register_uri(
            "GET",
            "mock://test.com/products/1/versions/1/urls",
            status_code=404,
            json=False,
        )
        with pytest.raises(
            CGWClientError,
            match="content gateway API returned error: " "\nstatus_code: 404, " "reason: None, " "error: false",
        ):
            cgw_client.get_urls(1, 1)
        assert m.call_count == 1


def test_get_single_url_success(cgw_client):
    test_url = {"url": "test/url"}
    with requests_mock.Mocker() as m:
        m.register_uri(
            "GET",
            "mock://test.com/products/1/versions/1/urls/1",
            status_code=200,
            json=test_url,
        )
        response = cgw_client.get_url(1, 1, 1)
        assert m.call_count == 1
        assert response == test_url


def test_create_url_success(cgw_client):
    test_url = {"url": "test/url"}
    with requests_mock.Mocker() as m:
        m.register_uri(
            "PUT",
            "mock://test.com/products/1/versions/1/urls/",
            status_code=200,
            json=test_url,
        )
        response = cgw_client.create_url(1, 1, test_url)
        assert m.call_count == 1
        assert response == test_url


def test_update_url_success(cgw_client):
    test_url = {"url": "test/url"}
    with requests_mock.Mocker() as m:
        m.register_uri(
            "POST",
            "mock://test.com/products/1/versions/1/urls",
            status_code=200,
            json=test_url,
        )
        response = cgw_client.update_url(1, 1, test_url)
        assert m.call_count == 1
        assert response == test_url


def test_delete_url_success(cgw_client):
    with requests_mock.Mocker() as m:
        m.register_uri(
            "DELETE",
            "mock://test.com/products/1/versions/1/urls/1",
            status_code=200,
        )
        cgw_client.delete_url(1, 1, 1)
        assert m.call_count == 1


def test_get_internals_success(cgw_client):
    test_internals = {"internals": "test/internals"}
    with requests_mock.Mocker() as m:
        m.register_uri(
            "GET",
            "mock://test.com/products/1/versions/1/internals",
            status_code=200,
            json=test_internals,
        )
        response = cgw_client.get_internals(1, 1)
        assert m.call_count == 1
        assert response == test_internals


def test_get_internals_failed(cgw_client):
    with requests_mock.Mocker() as m:
        m.register_uri(
            "GET",
            "mock://test.com/products/1/versions/1/internals",
            status_code=404,
            json=False,
        )
        with pytest.raises(
            CGWClientError,
            match="content gateway API returned error: " "\nstatus_code: 404, " "reason: None, " "error: false",
        ):
            cgw_client.get_internals(1, 1)
        assert m.call_count == 1


def test_get_single_internals_success(cgw_client):
    test_internals = {"internals": "test/internals"}
    with requests_mock.Mocker() as m:
        m.register_uri(
            "GET",
            "mock://test.com/products/1/versions/1/internals/1",
            status_code=200,
            json=test_internals,
        )
        response = cgw_client.get_internal(1, 1, 1)
        assert m.call_count == 1
        assert response == test_internals


def test_create_internals_success(cgw_client):
    test_internals = {"internals": "test/internals"}
    with requests_mock.Mocker() as m:
        m.register_uri(
            "PUT",
            "mock://test.com/products/1/versions/1/internals/",
            status_code=200,
            json=test_internals,
        )
        response = cgw_client.create_internal(1, 1, test_internals)
        assert m.call_count == 1
        assert response == test_internals


def test_update_internals_success(cgw_client):
    test_internals = {"internals": "test/internals"}
    with requests_mock.Mocker() as m:
        m.register_uri(
            "POST",
            "mock://test.com/products/1/versions/1/internals/",
            status_code=200,
            json=test_internals,
        )
        response = cgw_client.update_internal(1, 1, test_internals)
        assert m.call_count == 1
        assert response == test_internals


def test_delete_internals_success(cgw_client):
    with requests_mock.Mocker() as m:
        m.register_uri(
            "DELETE",
            "mock://test.com/products/1/versions/1/internals/1",
            status_code=200,
        )
        cgw_client.delete_internal(1, 1, 1)
        assert m.call_count == 1


def test_invalid_http_method_call(cgw_client):
    with requests_mock.Mocker() as m:
        m.register_uri(
            "INVALID_METHOD",
            "mock://test.com/products",
            json={"error": "An error has occurred!"},
        )
        with pytest.raises(CGWClientError, match="Wrong request method passed"):
            cgw_client.call_cgw_api("INVALID_METHOD", "/products")
        assert m.call_count == 0


def test_cgw_error_response():
    with requests_mock.Mocker() as m:
        m.register_uri(
            "GET",
            "/products",
            status_code=400,
            json={"error": "An error has occurred!"},
        )
        cgw_client = CGWClient("fake-host")
        with pytest.raises(CGWClientError):
            cgw_client.get_products()


def test_cgw_error_with_empty_host():
    with requests_mock.Mocker() as m:
        m.register_uri(
            "GET",
            "/products",
            status_code=400,
            json={"error": "An error has occurred!"},
        )

        with pytest.raises(CGWClientError, match="No content gateway hostname found"):
            CGWClient(None)
