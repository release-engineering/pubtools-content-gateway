import requests_mock
import pytest
from pubtools._content_gateway.push_base import PushBase, CGWError, FetcherDict
from tests.fake_cgw_client import TestClient

try:
    import mock
except ImportError:
    from unittest import mock


@pytest.fixture()
@mock.patch("pubtools._content_gateway.push_base.CGWClient", return_value=TestClient())
def push_base_object(mocked_cgw_client):
    push_base = PushBase("http://fake_host_nmae/test", "foo", "bar")
    return push_base


class TestPushBase:
    def test_create_product_1(self, create_product_data, push_base_object):
        push_base_object.process_product(create_product_data)
        assert push_base_object.cgw_client.create_product.calls == [((mock.ANY, create_product_data["metadata"]), {})]

    def test_create_product_2(self, create_product2_data, push_base_object):
        push_base_object.process_product(create_product2_data)
        assert (
            (mock.ANY, create_product2_data["metadata"]),
            {},
        ) in push_base_object.cgw_client.create_product.calls

    def test_create_duplicate_product(self, create_product_data, push_base_object):
        with pytest.raises(CGWError) as exception:
            push_base_object.process_product(create_product_data)
        assert str(exception.value) == "Cannot create new product. Record already present."

    def test_update_product(self, update_product_data, push_base_object):
        push_base_object.process_product(update_product_data)
        assert push_base_object.cgw_client.update_product.calls == [((mock.ANY, update_product_data["metadata"]), {})]

    def test_delete_product(self, delete_product_data, push_base_object):
        deleted_id = push_base_object.process_product(delete_product_data)
        assert push_base_object.cgw_client.delete_product.calls == [((mock.ANY, deleted_id), {})]

    def test_delete_invalid_product(self, delete_product_data, push_base_object):
        with pytest.raises(CGWError) as exception:
            push_base_object.process_product(delete_product_data)
        assert str(exception.value) == "Cannot update/delete the product %s %s, id is not set" % (
            delete_product_data["metadata"]["name"],
            delete_product_data["metadata"]["productCode"],
        )

    def test_create_version_1(self, create_version_data, push_base_object):
        push_base_object.process_version(create_version_data)
        assert push_base_object.cgw_client.create_version.calls == [
            ((mock.ANY, mock.ANY, create_version_data["metadata"]), {})
        ]

    def test_create_version_2(self, create_version2_data, push_base_object):
        push_base_object.process_version(create_version2_data)
        assert (
            (mock.ANY, mock.ANY, create_version2_data["metadata"]),
            {},
        ) in push_base_object.cgw_client.create_version.calls

    def test_create_duplicate_version(self, create_version_data, push_base_object):
        with pytest.raises(CGWError) as exception:
            push_base_object.process_version(create_version_data)
        assert str(exception.value) == "Cannot create new version. Record already present."

    def test_update_version(self, update_version_data, push_base_object):
        push_base_object.process_version(update_version_data)
        assert push_base_object.cgw_client.update_version.calls == [
            ((mock.ANY, mock.ANY, update_version_data["metadata"]), {})
        ]

    def test_delete_version(self, delete_version, push_base_object):
        deleted_id = push_base_object.process_version(delete_version)
        assert push_base_object.cgw_client.delete_version.calls == [((mock.ANY, mock.ANY, deleted_id), {})]

    def test_delete_invalid_version(self, delete_version, push_base_object):
        with pytest.raises(CGWError) as exception:
            push_base_object.process_version(delete_version)
        assert "Cannot update/delete the version name:" in str(exception.value)

    def test_create_version_without_product(self, create_version_without_product, push_base_object):
        with pytest.raises(CGWError) as exception:
            push_base_object.process_version(create_version_without_product)
        assert str(exception.value) == "Product name: %s product code: %s not found" % (
            create_version_without_product.get("metadata")["productName"],
            create_version_without_product.get("metadata")["productCode"],
        )

    def test_create_file_1(self, create_file_data, push_base_object):
        push_base_object.process_file(create_file_data)
        assert push_base_object.cgw_client.create_file.calls == [
            ((mock.ANY, mock.ANY, mock.ANY, create_file_data["metadata"]), {})
        ]

    def test_create_file_2(self, create_file2_data, push_base_object):
        push_base_object.process_file(create_file2_data)
        assert (
            (mock.ANY, mock.ANY, mock.ANY, create_file2_data["metadata"]),
            {},
        ) in push_base_object.cgw_client.create_file.calls

    def test_create_duplicate_file(self, create_file_data, push_base_object):
        with pytest.raises(CGWError) as exception:
            push_base_object.process_file(create_file_data)
        assert str(exception.value) == "Cannot create new file. Record already present."

    def test_update_file(self, update_file_data, push_base_object):
        push_base_object.process_file(update_file_data)
        assert push_base_object.cgw_client.update_file.calls == [
            ((mock.ANY, mock.ANY, mock.ANY, update_file_data["metadata"]), {})
        ]

    def test_delete_file(self, delete_file_data, push_base_object):
        deleted_id = push_base_object.process_file(delete_file_data)
        assert push_base_object.cgw_client.delete_file.calls == [((mock.ANY, mock.ANY, mock.ANY, deleted_id), {})]

    def test_delete_invalid_file(self, delete_file_data, push_base_object):
        with pytest.raises(CGWError) as exception:
            push_base_object.process_file(delete_file_data)
        assert "Cannot update/delete file: product version:" in str(exception.value)

    def test_create_file_without_product(self, create_file_without_product, push_base_object):
        with pytest.raises(CGWError) as exception:
            push_base_object.process_file(create_file_without_product)
        assert str(exception.value) == "Product name: %s product code: %s not found" % (
            create_file_without_product.get("metadata")["productName"],
            create_file_without_product.get("metadata")["productCode"],
        )

    def test_create_file_without_version(self, create_file_without_version, push_base_object):
        with pytest.raises(CGWError) as exception:
            push_base_object.process_file(create_file_without_version)
        assert str(exception.value) == "Product name: %s product code: %s version name: %s not found" % (
            create_file_without_version.get("metadata").get("productName"),
            create_file_without_version.get("metadata")["productCode"],
            create_file_without_version.get("metadata")["productVersionName"],
        )

    def test_invalid_product_mapping_key_check(self, push_base_object):
        with pytest.raises(ValueError) as exception:
            push_base_object.product_mapping.get(1)
        assert str(exception.value) == "key must be tuple (product, product_code)"

        with pytest.raises(ValueError) as exception:
            push_base_object.product_mapping.get((1,))
        assert str(exception.value) == "key must be tuple (product, product_code)"

    def test_invalid_product_version_mapping_key_check(self, push_base_object):
        with pytest.raises(ValueError) as exception:
            push_base_object.pv_mapping.get(1)
        assert str(exception.value) == "key must be tuple (product, product_code, product_version)"

        with pytest.raises(ValueError) as exception:
            push_base_object.pv_mapping.get((1,))
        assert str(exception.value) == "key must be tuple (product, product_code, product_version)"

    def test_invalid_file_mapping_key_check(self, push_base_object):
        with pytest.raises(ValueError) as exception:
            push_base_object.file_mapping.get(1)
        assert str(exception.value) == "key must be tuple (product, product_code, product_version, downloadURL)"

        with pytest.raises(ValueError) as exception:
            push_base_object.file_mapping.get((1,))
        assert str(exception.value) == "key must be tuple (product, product_code, product_version, downloadURL)"


class TestFetcherDict:
    def test_setitem(self, push_base_object):
        fetcher = FetcherDict({}, fetcher={}, key_checker=push_base_object._product_mapping_key_check)
        fetcher[("anything", "anything")] = "test"
        assert ("anything", "anything") in fetcher.data

    def test_getitem(self, push_base_object):
        fetcher = FetcherDict({}, fetcher={}, key_checker=push_base_object._product_mapping_key_check)
        fetcher[("anything", "anything")] = "test"
        result = fetcher[("anything", "anything")]
        assert "test" == result

    def test_getitem_with_empty_data(self, push_base_object):
        def fake_product(product_name, product_code):
            return {(("test_product_name", "test_product_code"), "test"): None}

        fetcher = FetcherDict(
            {},
            fetcher=fake_product,
            key_checker=push_base_object._product_mapping_key_check,
        )
        fetcher[("anything", "anything")] = "test"
        result = fetcher[("test_product_name", "test_product_code")]
        assert "test" == result

    def test_delitem(self, push_base_object):
        fetcher = FetcherDict({}, fetcher={}, key_checker=push_base_object._product_mapping_key_check)
        key = ("anything", "anything")
        fetcher[key] = "test"
        del fetcher[key]
        assert key not in fetcher.data


class TestRollbackOperations:
    @pytest.fixture()
    def push_base_object(self):
        push_base = PushBase("mock://test.com/", "foo", "bar")
        return push_base

    def test_rollback_created_product(self, push_base_object):
        data = {
            "type": "product",
            "state": "create",
            "product_id": 1234,
            "metadata": {
                # some data
            },
        }
        push_base_object.completed_operations = [data]
        with requests_mock.Mocker() as m:
            m.register_uri(
                "DELETE",
                "mock://test.com/products/1234",
                status_code=200,
            )
            push_base_object.rollback_cgw_operation()
            assert m.call_count == 1

    def test_rollback_updated_product(self, push_base_object):
        data = {
            "type": "product",
            "state": "update",
            "metadata": {
                "id": 1111,
                "name": "nameTest",
                "productCode": "productCodeTest",
                "homepage": "https://test.com/",
                "downloadpage": "https://testing.com/",
                "thankYouPage": "https://testing.com/",
                "eloquaCode": "NOT_SET",
                "featuredArtifactType": "Server",
                "thankYouTimeout": 3,
            },
        }
        push_base_object.completed_operations = [data]
        push_base_object.product_records[1111] = {"id": 1111}
        with requests_mock.Mocker() as m:
            m.register_uri(
                "POST",
                "mock://test.com/products",
                status_code=200,
            )
            push_base_object.rollback_cgw_operation()
            assert m.call_count == 1

    def test_rollback_created_version(self, push_base_object):
        data = {
            "type": "product_version",
            "state": "create",
            "version_id": 2222,
            "metadata": {
                "productId": 1111,
                "versionName": "TestName",
                # some other data
            },
        }
        push_base_object.completed_operations = [data]
        with requests_mock.Mocker() as m:
            m.register_uri(
                "DELETE",
                "mock://test.com/products/1111/versions/2222",
                status_code=200,
            )
            push_base_object.rollback_cgw_operation()
            assert m.call_count == 1

    def test_rollback_update_versions(self, push_base_object):
        data = {
            "type": "product_version",
            "state": "update",
            "metadata": {
                "id": 2222,
                "productId": 1111,
                "versionName": "AnsibleNewTestVersion 1",
                "ga": True,
                "masterProductVersion": None,
                "termsAndConditions": "Anonymous Download",
                "trackingDisabled": True,
                "hidden": True,
                "invisible": False,
                "releaseDate": "2022-25-05",
            },
        }
        push_base_object.version_records[data["metadata"]["id"]] = data["metadata"]
        push_base_object.completed_operations = [data]
        with requests_mock.Mocker() as m:
            m.register_uri(
                "POST",
                "mock://test.com/products/1111/versions",
                status_code=200,
            )
            push_base_object.rollback_cgw_operation()
            assert m.call_count == 1

    def test_rollback_created_file(self, push_base_object):
        data = {
            "type": "file",
            "state": "create",
            "product_id": 1111,
            "file_id": 333,
            "metadata": {
                "productVersionId": 2222,
                "downloadURL": "/content/origin/test",
                "description": "Red Hat OpenShift Local Sandbox Test",
                "label": "Checksum File Sandbox Test label",
                # some other data
            },
        }
        push_base_object.completed_operations = [data]
        with requests_mock.Mocker() as m:
            m.register_uri(
                "DELETE",
                "mock://test.com/products/1111/versions/2222/files/333",
                status_code=200,
            )
            push_base_object.rollback_cgw_operation()
            assert m.call_count == 1

    def test_rollback_update_files(self, push_base_object):
        data = {
            "type": "file",
            "state": "update",
            "product_id": 1111,
            "metadata": {
                "description": "Red Hat OpenShift Local Sandbox Test",
                "label": "Checksum File Sandbox Test label",
                "order": 0,
                "hidden": False,
                "invisible": False,
                "type": "FILE",
                "differentProductThankYouPage": None,
                "downloadURL": "/content/origin/test",
                "shortURL": "/pub-1/openshift-v4/testing",
                "md5": None,
                "size": None,
                "productVersionId": 2222,
                "id": 3333,
            },
        }
        push_base_object.file_records[data["metadata"]["id"]] = data["metadata"]
        push_base_object.completed_operations = [data]
        with requests_mock.Mocker() as m:
            m.register_uri(
                "POST",
                "mock://test.com/products/1111/versions/2222/files",
                status_code=200,
            )
            push_base_object.rollback_cgw_operation()
            assert m.call_count == 1


class TestMakeVisible:
    @pytest.fixture()
    def push_base_object(self):
        push_base = PushBase("mock://test.com/", "foo", "bar")
        return push_base

    def test_make_visible_created_version(self, push_base_object):
        data = {
            "type": "product_version",
            "state": "create",
            "version_id": 2222,
            "metadata": {
                "productId": 1111,
                "versionName": "AnsibleNewTestVersion 1",
                "ga": True,
                "masterProductVersion": None,
                "termsAndConditions": "Anonymous Download",
                "trackingDisabled": True,
                "hidden": True,
                "invisible": False,
                "releaseDate": "2022-25-05",
            },
        }
        push_base_object.completed_operations = [data]
        with requests_mock.Mocker() as m:
            m.register_uri(
                "POST",
                "mock://test.com/products/1111/versions",
                status_code=200,
            )
            push_base_object.make_visible()
            assert m.call_count == 1

    def test_make_visible_created_file(self, push_base_object):
        data = {
            "type": "file",
            "state": "create",
            "product_id": 1111,
            "file_id": 333,
            "metadata": {
                "hidden": False,
                "invisible": False,
                "type": "FILE",
                "downloadURL": "/content/origin/test",
                "shortURL": "/pub-1/openshift-v4/testing",
                "productVersionId": 2222,
            },
        }
        push_base_object.completed_operations = [data]
        with requests_mock.Mocker() as m:
            m.register_uri(
                "POST",
                "mock://test.com/products/1111/versions/2222/files",
                status_code=200,
            )
            push_base_object.make_visible()
            assert m.call_count == 1
