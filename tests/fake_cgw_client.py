from pubtools._content_gateway.cgw_client import CGWClientError
import six
import inspect


def tracker(f):
    calls = []

    def new_func(*args, **kwargs):
        calls.append((args, kwargs))
        return f(*args, **kwargs)

    new_func.calls = calls
    return new_func


class TestClientMeta(type):
    def __new__(cls, clsname, bases, attrs):
        new_attrs = {}
        missing = set(bases[0].__dict__.keys()) - set(list(attrs.keys()) + ["call_cgw_api"])
        missing = [x for x in missing if not x.startswith("_")]
        if missing:
            raise KeyError("TestClient is missing following attributes:%s" % missing)

        for k, v in attrs.items():
            if k.startswith("__"):
                new_attrs[k] = v
            elif inspect.isfunction(v):
                new_attrs[k] = tracker(v)
            else:
                new_attrs[k] = v
        return type.__new__(cls, clsname, bases, new_attrs)


@six.add_metaclass(TestClientMeta)
class TestClient(object):
    def __init__(self, *args, **kwargs):
        self.products = {}
        self.product_versions = {}
        self.files = {}
        self.pid_counter = 0
        self.pvid_counter = 0
        self.fid_counter = 0

    def get_products(self, params=None):
        return self.products.values()

    def get_product(self, pid, params=None):
        if pid not in self.products:
            raise CGWClientError(
                "content gateway API returned error: " "\nstatus_code: 404, reason: %s" % ("product not found")
            )
        return self.products[pid]

    def create_product(self, data):
        self.pid_counter += 1
        data["id"] = self.pid_counter
        self.products[self.pid_counter] = data
        self.product_versions[self.pid_counter] = {}
        self.files[self.pid_counter] = {}
        return self.pid_counter

    def update_product(self, data):
        if data["id"] not in self.products:
            raise CGWClientError(
                "content gateway API returned error: " "\nstatus_code: 404, reason: %s" % ("product not found")
            )
        self.products[data["id"]] = data

    def delete_product(self, pid, params=None):
        if pid not in self.products:
            raise CGWClientError(
                "content gateway API returned error: " "\nstatus_code: 404, reason: %s" % ("product not found")
            )
        if self.product_versions[pid]:
            raise CGWClientError(
                "content gateway API returned error: "
                "\nstatus_code: 400, reason: %s" % ("product versions are not empty")
            )
        self.products.pop(pid)

    def get_versions(self, pid, params=None):
        if pid not in self.products:
            raise CGWClientError(
                "content gateway API returned error: "
                "\nstatus_code: 404, reason: product %s not found" % self.products
            )
        return list(self.product_versions[pid].values())

    def get_version(self, pid, vid, params=None):
        if pid not in self.products:
            raise CGWClientError(
                "content gateway API returned error: " "\nstatus_code: 404, reason: %s" % ("product not found")
            )
        if vid not in self.product_versions[pid]:
            raise CGWClientError(
                "content gateway API returned error: " "\nstatus_code: 404, reason: %s" % ("version not found")
            )
        return self.product_versions[pid][vid]

    def create_version(self, pid, data):
        if pid not in self.products:
            raise CGWClientError(
                "content gateway API returned error: " "\nstatus_code: 404, reason: %s" % ("product not found")
            )
        self.pvid_counter += 1
        data["id"] = self.pvid_counter
        self.product_versions[pid][self.pvid_counter] = data
        self.files[pid][self.pvid_counter] = {}
        return self.pvid_counter

    def update_version(self, pid, data):
        if pid not in self.products:
            raise CGWClientError(
                "content gateway API returned error: " "\nstatus_code: 404, reason: %s" % ("product not found")
            )
        if data["id"] not in self.product_versions:
            raise CGWClientError(
                "content gateway API returned error: " "\nstatus_code: 404, reason: %s" % ("version not found")
            )
        self.product_versions[pid][data["id"]] = data

    def delete_version(self, pid, vid, params=None):
        if pid not in self.product_versions:
            raise CGWClientError(
                "content gateway API returned error: " "\nstatus_code: 404, reason: %s" % ("product not found")
            )
        if vid not in self.product_versions[pid]:
            raise CGWClientError(
                "content gateway API returned error: " "\nstatus_code: 404, reason: %s" % ("version not found")
            )
        if self.files[pid][vid]:
            raise CGWClientError(
                "content gateway API returned error: "
                "\nstatus_code: 400, reason: %s" % ("version files are non empty")
            )
        self.product_versions[pid].pop(vid)
        self.files[pid].pop(vid)

    def get_all_files(self, pid, vid, params=None):
        if pid not in self.files:
            raise CGWClientError(
                "content gateway API returned error: " "\nstatus_code: 404, reason: %s" % ("product not found")
            )
        if vid not in self.files[pid]:
            raise CGWClientError(
                "content gateway API returned error: " "\nstatus_code: 404, reason: %s" % ("version not found")
            )
        return self.files[pid][vid]

    def get_files(self, pid, vid, params=None):
        if pid not in self.files:
            raise CGWClientError(
                "content gateway API returned error: " "\nstatus_code: 404, reason: %s" % ("product not found")
            )
        if vid not in self.files[pid]:
            raise CGWClientError(
                "content gateway API returned error: " "\nstatus_code: 404, reason: %s" % ("version not found")
            )
        # return self.files[pid][vid]
        return list(self.files[pid][vid].values())

    def get_file(self, pid, vid, fid, params=None):
        if pid not in self.files:
            raise CGWClientError(
                "content gateway API returned error: " "\nstatus_code: 404, reason: %s" % ("product not found")
            )
        if vid not in self.files[pid]:
            raise CGWClientError(
                "content gateway API returned error: " "\nstatus_code: 404, reason: %s" % ("version not found")
            )
        if fid not in self.files[pid][vid]:
            raise CGWClientError(
                "content gateway API returned error: " "\nstatus_code: 404, reason: %s" % ("file not found")
            )
        return self.files[pid][vid][fid]

    def create_file(self, pid, vid, data):
        if pid not in self.files:
            raise CGWClientError(
                "content gateway API returned error: " "\nstatus_code: 404, reason: %s" % ("product not found")
            )
        if vid not in self.files[pid]:
            raise CGWClientError(
                "content gateway API returned error: " "\nstatus_code: 404, reason: %s" % ("version not found")
            )
        self.fid_counter += 1
        data["id"] = self.fid_counter
        self.files[pid][vid][self.fid_counter] = data
        return self.fid_counter

    def update_file(self, pid, vid, data):
        if pid not in self.files:
            raise CGWClientError(
                "content gateway API returned error: " "\nstatus_code: 404, reason: %s" % ("product not found")
            )
        if vid not in self.files[pid]:
            raise CGWClientError(
                "content gateway API returned error: " "\nstatus_code: 404, reason: %s" % ("version not found")
            )
        if data["id"] not in self.files:
            raise CGWClientError(
                "content gateway API returned error: " "\nstatus_code: 404, reason: %s" % ("file not found")
            )
        self.files[pid][vid][data["id"]] = data

    def delete_file(self, pid, vid, fid, data=None):
        if pid not in self.files:
            raise CGWClientError(
                "content gateway API returned error: " "\nstatus_code: 404, reason: %s" % ("product not found")
            )
        if vid not in self.files[pid]:
            raise CGWClientError(
                "content gateway API returned error: " "\nstatus_code: 404, reason: %s" % ("version not found")
            )
        if fid not in self.files[pid][vid]:
            raise CGWClientError(
                "content gateway API returned error: " "\nstatus_code: 404, reason: %s" % ("file not found")
            )
        self.files[pid][vid].pop(fid)
