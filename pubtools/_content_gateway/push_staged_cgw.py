from pushsource import CGWPushItem
from .push_base import PushBase
from .utils import yaml_parser, validate_data, sort_items
from attrs import asdict
import pluggy
import json
import os

pm = pluggy.PluginManager("pubtools")
hookspec = pluggy.HookspecMarker("pubtools")
hookimpl = pluggy.HookimplMarker("pubtools")


class PushStagedCGW(PushBase):
    def __init__(self, target_name, target_settings):
        PushBase.__init__(self,
                          target_settings['server_name'],
                          target_settings['username'],
                          target_settings['password'])
        self.push_items = []
        self.pulp_push_items = {}

    @hookimpl
    def gather_source_items(self, pulp_push_item, push_item):
        self.push_items.append(push_item)
        self.pulp_push_items[json.dumps(asdict(push_item), sort_keys=True)] = pulp_push_item

    def push_staged_operations(self):
        for item in self.push_items:
            if isinstance(item, CGWPushItem):
                parsed_items = yaml_parser(os.path.join(item.origin, item.src))
                for pitem in parsed_items:
                    validate_data(pitem, staged=True)

                parsed_items = sort_items(parsed_items)
                for pitem in parsed_items:
                    if pitem['type'] == 'product':
                        self.process_product(pitem)
                    if pitem.get('type') == 'product_version':
                        self.process_version(pitem)
                    if pitem['type'] == 'file':
                        for push_item in self.push_items:
                            if push_item.src == pitem['metadata']['pushItemPath']:
                                break
                        else:
                            raise ValueError("Unable to find push item with path:%s" % pitem['metadata']['pushItemPath'])
                        pulp_push_item = self.pulp_push_items[json.dumps(asdict(item), sort_keys=True)]
                        pitem['metadata']['downloadURL'] = pulp_push_item.cdn_path
                        pitem['metadata']['md5'] = item.md5sum
                        pitem['metadata']['sha256'] = pulp_push_item.sha256sum
                        pitem['metadata']['size'] = pulp_push_item.size

                        self.process_file(pitem)


def entry_point(target_name, target_settings):
    push_staged = PushStagedCGW(target_name, target_settings)
    return push_staged
