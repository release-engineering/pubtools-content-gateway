from pushsource import CGWPushItem
from .push_base import PushBase
from .utils import yaml_parser
import logging
from attrs import asdict
import pluggy
import json

pm = pluggy.PluginManager("pubtools")
hookspec = pluggy.HookspecMarker("pubtools")
hookimpl = pluggy.HookimplMarker("pubtools")

LOG = logging.getLogger("pubtools.cgw")
LOG_FORMAT = "%(asctime)s [%(levelname)-8s] %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)


class PushStagedCGW(PushBase):
    def __init__(self, target_name, target_settings):
        PushBase.__init__(self, target_settings['server_name'], target_settings['username'],
                          target_settings['password'])
        self.push_items = []
        self.pulp_push_items = {}

    @hookimpl
    def gather_source_items(self, pulp_push_item, push_item):
        self.push_items.append(push_item)
        self.pulp_push_items[json.dumps(asdict(push_item), sort_keys=True)] = pulp_push_item

    def push_staged_operations(self):
        cgw_products = self.cgw_client.get_products()
        for item in self.push_items:
            if isinstance(item, CGWPushItem):
                parsed_items = yaml_parser(item.src)
                for data in cgw_products:
                    self.product_mapping[(data['name'], data['productCode'])] = data['id']
                for pitem in parsed_items:
                    if pitem['type'] == 'product':
                        self.process_product(pitem)
                    if pitem.get('type') == 'product_version':
                        if not self.pv_mapping:
                            self._create_product_version_mapping(pitem.get('metadata')['productName'],
                                                                 pitem.get('metadata')['productCode'])
                        self.process_version(pitem)
                    if pitem['type'] == 'file':
                        self.process_file(pitem, True)


def entry_point(target_name, target_settings):
    push_staged = PushStagedCGW(target_name, target_settings)
    return push_staged
