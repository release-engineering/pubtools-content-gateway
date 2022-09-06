import pytest


@pytest.fixture
def fixture_unsorted_files_json():
    json = [
        {
            "type": "product",
            "state": "create",
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
            "state": "create",
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
            "state": "delete",
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
            "state": "delete",
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
            "state": "create",
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
            "state": "delete",
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
            "state": "create",
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
            "state": "create",
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
            "state": "create",
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
            "state": "delete",
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
            "state": "delete",
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
            "state": "delete",
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
        "state": "create",
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
        "state": "create",
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
        "state": "update",
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
        "state": "delete",
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
        "state": "create",
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
        "state": "update",
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
        "state": "create",
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
        "state": "create",
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
        "state": "delete",
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
        "state": "create",
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
        "state": "create",
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
        "state": "create",
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
        "state": "create",
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
        "state": "update",
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
        "state": "delete",
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
