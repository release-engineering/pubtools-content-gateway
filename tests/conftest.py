import os

import pytest

from pushsource import Source


@pytest.fixture
def fixture_unsorted_files_json():
    json = [
        {
            "type": "product",
            "action": "create",
            "metadata": {
                "name": "Cloud: Ansible NEW Test",
                "productCode": "AnsibleNewTest",
                "homepage": "https://test.com/",
                "downloadpage": "https://test.com/",
                "thankYouPage": "https://test.com/",
                "eloquaCode": "NOT_SET",
                "featuredArtifactType": "Server",
                "thankYouTimeout": 5,
            },
        },
        {
            "type": "product_version",
            "action": "create",
            "metadata": {
                "productName": "Cloud: Ansible NEW Test",
                "productCode": "AnsibleNewTest",
                "versionName": "AnsibleNewTestVersion",
                "ga": True,
                "masterProductVersion": None,
                "termsAndConditions": "Anonymous Download",
                "trackingDisabled": False,
                "hidden": False,
                "invisible": False,
                "releaseDate": "2022-25-05",
            },
        },
        {
            "type": "product",
            "action": "delete",
            "metadata": {
                "name": "Cloud: Ansible NEW Test 2",
                "productCode": "AnsibleNewTest",
                "homepage": "https://test.com/",
                "downloadpage": "https://test.com/",
                "thankYouPage": "https://test.com/",
                "eloquaCode": "NOT_SET",
                "featuredArtifactType": "Server",
                "thankYouTimeout": 5,
            },
        },
        {
            "type": "product_version",
            "action": "delete",
            "metadata": {
                "productName": "Cloud: Ansible NEW Test 2",
                "productCode": "AnsibleNewTest",
                "versionName": "AnsibleNewTestVersion",
                "ga": True,
                "masterProductVersion": None,
                "termsAndConditions": "Anonymous Download",
                "trackingDisabled": False,
                "hidden": False,
                "invisible": False,
                "releaseDate": "2022-25-05",
            },
        },
        {
            "type": "file",
            "action": "create",
            "metadata": {
                "productName": "Cloud: Ansible NEW TEST",
                "productCode": "AnsibleNewTest",
                "productVersionName": "AnsibleNewTestVersion",
                "description": "Red Hat OpenShift Local Sandbox Test",
                "label": "Checksum File Sandbox Test",
                "order": 0,
                "hidden": False,
                "invisible": False,
                "type": "FILE",
                "differentProductThankYouPage": None,
                "downloadURL": "/content/origin/files/sha256/92/AnsibleNewTest/sha256sum",
                "shortURL": "/pub-1/openshift-v4/clients/AnsibleNewTest/sha256sum",
                "md5": None,
                "size": None,
            },
        },
        {
            "type": "file",
            "action": "delete",
            "metadata": {
                "productName": "Cloud: Ansible NEW TESTTEST",
                "productCode": "AnsibleNewTest",
                "productVersionName": "AnsibleNewTestVersion",
                "description": "Red Hat OpenShift Local Sandbox Test",
                "label": "Checksum File Sandbox Test",
                "order": 0,
                "hidden": False,
                "invisible": False,
                "type": "FILE",
                "differentProductThankYouPage": None,
                "downloadURL": "/content/origin/files/sha256/92/AnsibleNewTest/sha256sum",
                "shortURL": "/pub-1/openshift-v4/clients/AnsibleNewTest/sha256sum",
                "md5": None,
                "size": None,
            },
        },
    ]
    return json


@pytest.fixture
def fixture_sorted_files_json():
    json = [
        {
            "type": "product",
            "action": "create",
            "metadata": {
                "name": "Cloud: Ansible NEW Test",
                "productCode": "AnsibleNewTest",
                "homepage": "https://test.com/",
                "downloadpage": "https://test.com/",
                "thankYouPage": "https://test.com/",
                "eloquaCode": "NOT_SET",
                "featuredArtifactType": "Server",
                "thankYouTimeout": 5,
            },
        },
        {
            "type": "product_version",
            "action": "create",
            "metadata": {
                "productName": "Cloud: Ansible NEW Test",
                "productCode": "AnsibleNewTest",
                "versionName": "AnsibleNewTestVersion",
                "ga": True,
                "masterProductVersion": None,
                "termsAndConditions": "Anonymous Download",
                "trackingDisabled": False,
                "hidden": False,
                "invisible": False,
                "releaseDate": "2022-25-05",
            },
        },
        {
            "type": "file",
            "action": "create",
            "metadata": {
                "productName": "Cloud: Ansible NEW TEST",
                "productCode": "AnsibleNewTest",
                "productVersionName": "AnsibleNewTestVersion",
                "description": "Red Hat OpenShift Local Sandbox Test",
                "label": "Checksum File Sandbox Test",
                "order": 0,
                "hidden": False,
                "invisible": False,
                "type": "FILE",
                "differentProductThankYouPage": None,
                "downloadURL": "/content/origin/files/sha256/92/AnsibleNewTest/sha256sum",
                "shortURL": "/pub-1/openshift-v4/clients/AnsibleNewTest/sha256sum",
                "md5": None,
                "size": None,
            },
        },
        {
            "type": "file",
            "action": "delete",
            "metadata": {
                "productName": "Cloud: Ansible NEW TESTTEST",
                "productCode": "AnsibleNewTest",
                "productVersionName": "AnsibleNewTestVersion",
                "description": "Red Hat OpenShift Local Sandbox Test",
                "label": "Checksum File Sandbox Test",
                "order": 0,
                "hidden": False,
                "invisible": False,
                "type": "FILE",
                "differentProductThankYouPage": None,
                "downloadURL": "/content/origin/files/sha256/92/AnsibleNewTest/sha256sum",
                "shortURL": "/pub-1/openshift-v4/clients/AnsibleNewTest/sha256sum",
                "md5": None,
                "size": None,
            },
        },
        {
            "type": "product_version",
            "action": "delete",
            "metadata": {
                "productName": "Cloud: Ansible NEW Test 2",
                "productCode": "AnsibleNewTest",
                "versionName": "AnsibleNewTestVersion",
                "ga": True,
                "masterProductVersion": None,
                "termsAndConditions": "Anonymous Download",
                "trackingDisabled": False,
                "hidden": False,
                "invisible": False,
                "releaseDate": "2022-25-05",
            },
        },
        {
            "type": "product",
            "action": "delete",
            "metadata": {
                "name": "Cloud: Ansible NEW Test 2",
                "productCode": "AnsibleNewTest",
                "homepage": "https://test.com/",
                "downloadpage": "https://test.com/",
                "thankYouPage": "https://test.com/",
                "eloquaCode": "NOT_SET",
                "featuredArtifactType": "Server",
                "thankYouTimeout": 5,
            },
        },
    ]
    return json


@pytest.fixture
def create_product_data():
    return {
        "type": "product",
        "action": "create",
        "metadata": {
            "name": "Cloud: Ansible NEW Test",
            "productCode": "AnsibleNewTest",
            "homepage": "https://test.com/",
            "downloadpage": "https://test.com/",
            "thankYouPage": "https://test.com/",
            "eloquaCode": "NOT_SET",
            "featuredArtifactType": "Server",
            "thankYouTimeout": 5,
        },
    }


@pytest.fixture
def create_product2_data():
    return {
        "type": "product",
        "action": "create",
        "metadata": {
            "name": "Cloud: Ansible NEW Test 1",
            "productCode": "AnsibleNewTest 1",
            "homepage": "https://test.com/",
            "downloadpage": "https://test.com/",
            "thankYouPage": "https://test.com/",
            "eloquaCode": "NOT_SET",
            "featuredArtifactType": "Server",
            "thankYouTimeout": 5,
        },
    }


@pytest.fixture
def update_product_data():
    return {
        "type": "product",
        "action": "update",
        "metadata": {
            "name": "Cloud: Ansible NEW Test",
            "productCode": "AnsibleNewTest",
            "homepage": "https://test.fixture.com/",
            "downloadpage": "https://test.fixture.com/",
            "thankYouPage": "https://test.fixture.com/",
            "eloquaCode": "NOT_SET",
            "featuredArtifactType": "Server",
            "thankYouTimeout": 5,
        },
    }


@pytest.fixture
def delete_product_data():
    return {
        "type": "product",
        "action": "delete",
        "metadata": {
            "name": "Cloud: Ansible NEW Test 1",
            "productCode": "AnsibleNewTest 1",
            "homepage": "https://test.com/",
            "downloadpage": "https://test.com/",
            "thankYouPage": "https://test.com/",
            "eloquaCode": "NOT_SET",
            "featuredArtifactType": "Server",
            "thankYouTimeout": 5,
        },
    }


@pytest.fixture
def create_version_data():
    return {
        "type": "product_version",
        "action": "create",
        "metadata": {
            "productName": "Cloud: Ansible NEW Test",
            "productCode": "AnsibleNewTest",
            "versionName": "AnsibleNewTestVersion",
            "ga": True,
            "masterProductVersion": None,
            "termsAndConditions": "Anonymous Download",
            "trackingDisabled": False,
            "hidden": False,
            "invisible": False,
            "releaseDate": "2022-25-05",
        },
    }


@pytest.fixture
def update_version_data():
    return {
        "type": "product_version",
        "action": "update",
        "metadata": {
            "productName": "Cloud: Ansible NEW Test",
            "productCode": "AnsibleNewTest",
            "versionName": "AnsibleNewTestVersion",
            "ga": True,
            "masterProductVersion": None,
            "termsAndConditions": "Anonymous Download",
            "trackingDisabled": False,
            "hidden": False,
            "invisible": False,
            "releaseDate": "2022-25-05",
        },
    }


@pytest.fixture
def create_version2_data():
    return {
        "type": "product_version",
        "action": "create",
        "metadata": {
            "productName": "Cloud: Ansible NEW Test",
            "productCode": "AnsibleNewTest",
            "versionName": "AnsibleNewTestVersion 2",
            "ga": True,
            "masterProductVersion": None,
            "termsAndConditions": "Anonymous Download",
            "trackingDisabled": False,
            "hidden": False,
            "invisible": False,
            "releaseDate": "2022-25-05",
        },
    }


@pytest.fixture
def create_version_without_product():
    return {
        "type": "product_version",
        "action": "create",
        "metadata": {
            "productName": "InvalidProduct",
            "productCode": "InvalidProduct",
            "versionName": "InvalidProductVersion",
            "ga": True,
            "masterProductVersion": None,
            "termsAndConditions": "Anonymous Download",
            "trackingDisabled": False,
            "hidden": False,
            "invisible": False,
            "releaseDate": "2022-25-05",
        },
    }


@pytest.fixture
def delete_version():
    return {
        "type": "product_version",
        "action": "delete",
        "metadata": {
            "productName": "Cloud: Ansible NEW Test",
            "productCode": "AnsibleNewTest",
            "versionName": "AnsibleNewTestVersion 2",
            "ga": True,
            "masterProductVersion": None,
            "termsAndConditions": "Anonymous Download",
            "trackingDisabled": False,
            "hidden": False,
            "invisible": False,
            "releaseDate": "2022-25-05",
        },
    }


@pytest.fixture
def create_file_data():
    return {
        "type": "file",
        "action": "create",
        "metadata": {
            "productName": "Cloud: Ansible NEW Test",
            "productCode": "AnsibleNewTest",
            "productVersionName": "AnsibleNewTestVersion",
            "description": "Red Hat OpenShift Local Sandbox Test",
            "label": "Checksum File Sandbox Test",
            "order": 0,
            "hidden": False,
            "invisible": False,
            "type": "FILE",
            "differentProductThankYouPage": None,
            "downloadURL": "/test/download/url",
            "shortURL": "/test/AnsibleNewTest/sha256sum",
            "md5": None,
            "size": None,
        },
    }


@pytest.fixture
def create_file_without_product():
    return {
        "type": "file",
        "action": "create",
        "metadata": {
            "productName": "Invalid product name",
            "productCode": "InvalidCode",
            "productVersionName": "InvalidVersion",
            "description": "Red Hat OpenShift Local Sandbox Test",
            "label": "Checksum File Sandbox Test",
            "order": 0,
            "hidden": False,
            "invisible": False,
            "type": "FILE",
            "differentProductThankYouPage": None,
            "downloadURL": "/test/download/url",
            "shortURL": "/test/AnsibleNewTest/sha256sum",
            "md5": None,
            "size": None,
        },
    }


@pytest.fixture
def create_file_without_version():
    return {
        "type": "file",
        "action": "create",
        "metadata": {
            "productName": "Cloud: Ansible NEW Test",
            "productCode": "AnsibleNewTest",
            "productVersionName": "InvalidVersion",
            "description": "Red Hat OpenShift Local Sandbox Test",
            "label": "Checksum File Sandbox Test",
            "order": 0,
            "hidden": False,
            "invisible": False,
            "type": "FILE",
            "differentProductThankYouPage": None,
            "downloadURL": "/test/download/url",
            "shortURL": "/test/AnsibleNewTest/sha256sum",
            "md5": None,
            "size": None,
        },
    }


@pytest.fixture
def create_file2_data():
    return {
        "type": "file",
        "action": "create",
        "metadata": {
            "productName": "Cloud: Ansible NEW Test",
            "productCode": "AnsibleNewTest",
            "productVersionName": "AnsibleNewTestVersion",
            "description": "Red Hat OpenShift Local Sandbox Test 2",
            "label": "Checksum File Sandbox Test",
            "order": 0,
            "hidden": False,
            "invisible": False,
            "type": "FILE",
            "differentProductThankYouPage": None,
            "downloadURL": "/test/download/url/2",
            "shortURL": "/test/Second/AnsibleTest/sha256sum",
            "md5": None,
            "size": None,
        },
    }


@pytest.fixture
def update_file_data():
    return {
        "type": "file",
        "action": "update",
        "metadata": {
            "productName": "Cloud: Ansible NEW Test",
            "productCode": "AnsibleNewTest",
            "productVersionName": "AnsibleNewTestVersion",
            "description": "Red Hat OpenShift Local Sandbox Test 3",
            "label": "Checksum File Sandbox Test Updated",
            "order": 0,
            "hidden": False,
            "invisible": False,
            "type": "FILE",
            "differentProductThankYouPage": None,
            "downloadURL": "/test/download/url/2",
            "shortURL": "/test/Second/AnsibleTest/sha256sum",
            "md5": None,
            "size": None,
        },
    }


@pytest.fixture
def delete_file_data():
    return {
        "type": "file",
        "action": "delete",
        "metadata": {
            "productName": "Cloud: Ansible NEW Test",
            "productCode": "AnsibleNewTest",
            "productVersionName": "AnsibleNewTestVersion",
            "description": "Red Hat OpenShift Local Sandbox Test 2",
            "label": "Checksum File Sandbox Test",
            "order": 0,
            "hidden": False,
            "invisible": False,
            "type": "FILE",
            "differentProductThankYouPage": None,
            "downloadURL": "/test/download/url/2",
            "shortURL": "/test/Second/AnsibleTest/sha256sum",
            "md5": None,
            "size": None,
        },
    }


@pytest.fixture
def yml_json_data():
    # This data will be used to verify the hybrid model of yml structure.
    # The yml file can accept both linear and nested yml data structure.
    # The nested yml data will get converted to linear format inorder to process

    json = [
        {
            "type": "product",
            "action": "create",
            "metadata": {
                "name": "Product_Name_1",
                "productCode": "Product_code_1",
                "homepage": "https://developers.redhat.com/products/codeready-containers/overview/",
                "downloadpage": "https://developers.redhat.com/products/codeready-containers/download/",
                "thankYouPage": "https://test.com/",
                "thankYouTimeout": 5,
                "eloquaCode": "FAKECODEID1234",
            },
        },
        {
            "type": "product_version",
            "action": "create",
            "metadata": {
                "versionName": "3.4.0",
                "masterProductVersion": None,
                "releaseDate": "2022-25-05",
                "ga": True,
                "hidden": False,
                "invisible": False,
                "trackingDisabled": False,
                "termsAndConditions": "Anonymous Download",
                "productName": "Product_Name_1",
                "productCode": "Product_code_1",
            },
        },
        {
            "type": "file",
            "action": "create",
            "metadata": {
                "downloadURL": "/content/origin/files/AnsibleNewTest_1/",
                "label": "Checksum File",
                "shortURL": "/pub/openshift-v1/clients/sha256sum.txt",
                "description": "Red Hat OpenShift Local",
                "differentProductThankYouPage": None,
                "order": 10,
                "productName": "Product_Name_1",
                "productCode": "Product_code_1",
                "productVersionName": "3.4.0",
            },
        },
        {
            "type": "file",
            "action": "create",
            "metadata": {
                "downloadURL": "/content/origin/files/AnsibleNewTest_2/",
                "label": "Release Info",
                "shortURL": "/pub/openshift-v2/clients/sha256sum.txt",
                "description": "Red Hat OpenShift Local",
                "differentProductThankYouPage": None,
                "order": 20,
                "productName": "Product_Name_1",
                "productCode": "Product_code_1",
                "productVersionName": "3.4.0",
            },
        },
        {
            "type": "product",
            "action": "create",
            "metadata": {
                "name": "Cloud: Ansible NEW Test 1",
                "productCode": "AnsibleNewTest",
                "homepage": "https://test.com/",
                "downloadpage": "https://test.com/",
                "thankYouPage": "https://test.com/",
                "eloquaCode": "NOT_SET",
                "featuredArtifactType": "Server",
                "thankYouTimeout": 5,
            },
        },
        {
            "type": "product_version",
            "action": "create",
            "metadata": {
                "productName": "Cloud: Ansible NEW Test 1",
                "productCode": "AnsibleNewTest",
                "versionName": "AnsibleNewTestVersion 1",
                "ga": True,
                "masterProductVersion": None,
                "termsAndConditions": "Anonymous Download",
                "trackingDisabled": False,
                "hidden": False,
                "invisible": False,
                "releaseDate": "2022-25-05",
            },
        },
        {
            "type": "file",
            "action": "create",
            "metadata": {
                "productName": "Cloud: Ansible NEW Test 1",
                "productCode": "AnsibleNewTest",
                "productVersionName": "AnsibleNewTestVersion 1",
                "description": "Red Hat OpenShift Local Sandbox Test",
                "label": "Checksum File Sandbox Test",
                "order": 0,
                "hidden": False,
                "invisible": False,
                "type": "FILE",
                "differentProductThankYouPage": None,
                "downloadURL": "/content/origin/test",
                "shortURL": "/pub-1/openshift-v4/test",
                "md5": None,
                "size": None,
            },
        },
    ]
    return json


def test_staging_dir():
    return os.path.join(os.path.dirname(__file__), "test_data/test_staging_dir")


@pytest.fixture()
def fixture_source_stage(request):
    yield Source.register_backend("stage", lambda: request.param)
    Source.reset()
