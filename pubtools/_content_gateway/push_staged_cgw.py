import os
import json
import logging
from .push_base import PushBase
from .utils import yaml_parser, validate_data, sort_items, format_cgw_items

try:
    import attr as attrs
except ImportError:  # pragma: no cover
    import attrs

from pubtools.pluggy import hookimpl, pm
from pushsource import CGWPushItem
from pushsource import Source

LOG = logging.getLogger("pubtools.cgw")
LOG_FORMAT = "%(asctime)s [%(levelname)-8s] %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)


class PushStagedCGW(PushBase):
    """Handle push staged CGW workflow."""

    def __init__(self, source_urls, target_name, target_settings):
        """
        Initialize.

        Args:
            target_name (str):
                Name of the target.
            target_settings (dict):
                Target settings.
        """
        PushBase.__init__(
            self,
            target_settings["target_address"],
            target_settings["target_user"],
            target_settings["target_password"],
        )
        self.push_items = []
        self.pulp_push_units = {}
        self.processed_push_items = {}
        self.source_urls = source_urls

        for source_url in source_urls:
            with Source.get(source_url) as source:
                LOG.info("Loading items from %s", source_url)
                for item in source:
                    self.push_items.append(item)

    @staticmethod
    def push_item_str(item):
        push_item_dict = attrs.asdict(item)
        item_json = {
            "name": push_item_dict["name"],
            "src": push_item_dict["src"],
            "dest": push_item_dict["dest"],
            "origin": push_item_dict["origin"],
            "build": push_item_dict["build"],
            "signing_key": push_item_dict["signing_key"],
        }
        return json.dumps(item_json, sort_keys=True)

    @hookimpl
    def pulp_item_push_finished(self, pulp_units, push_item):
        """
        Invoked during task execution after successful completion of all Pulp
        publishes.

        This hook is invoked for every push item, to indicate that all Pulp
        content associated with the task is considered fully up-to-date. The
        intended usage is to flush Pulp-derived caches or to notify systems that
        Pulp content may have recently changed.

        Args:
            pulp_push_item (Pulp object):
                push item from the pulp.
            push_item (list):
                push item.
        """

        if pulp_units:
            self.pulp_push_units[self.push_item_str(push_item)] = pulp_units[0]
            self.processed_push_items[self.push_item_str(push_item)] = push_item

    def push_staged_operations(self):
        """
        Initiate the CGW operations for push staged.
        Operations such as create, update or delete
        on products, versions and files would be performed.
        """

        for item in self.push_items:
            if isinstance(item, CGWPushItem):
                parsed_items = yaml_parser(os.path.join(item.origin, item.src))
                parsed_items = format_cgw_items(parsed_items)

                for pitem in parsed_items:
                    validate_data(pitem, staged=True)

                parsed_items = sort_items(parsed_items)
                try:
                    for pitem in parsed_items:
                        if pitem["type"] == "product":
                            self.process_product(pitem)
                        if pitem.get("type") == "product_version":
                            self.process_version(pitem)
                        if pitem["type"] == "file":
                            for push_item in self.push_items:
                                found = False
                                for source_url in self.source_urls:
                                    if (
                                        push_item.src.replace(push_item.origin, "").lstrip("/")
                                        == pitem["metadata"]["pushItemPath"]
                                    ):
                                        found = True
                                if found:
                                    break
                            else:
                                raise ValueError(
                                    "Unable to find push item with path:%s" % pitem["metadata"]["pushItemPath"]
                                )
                            pulp_push_unit = self.pulp_push_units[self.push_item_str(push_item)]
                            pulp_push_item = self.processed_push_items[self.push_item_str(push_item)]
                            pitem["metadata"]["downloadURL"] = pulp_push_unit.cdn_path
                            pitem["metadata"]["md5"] = pulp_push_item.md5sum
                            pitem["metadata"]["sha256"] = pulp_push_unit.sha256sum
                            pitem["metadata"]["size"] = os.stat(push_item.src).st_size
                            self.process_file(pitem)

                    self.make_visible()
                    LOG.info("\n All CGW operations are successfully completed...!")
                except Exception as error:
                    LOG.exception("Exception occurred during the CGW operation %s" % error)
                    LOG.info("Rolling back the partial operation")
                    self.rollback_cgw_operation()

                    #  raising the occurred Exception as all the exception will get caught in this except block
                    #  we want to return full Traceback
                    raise error


def entry_point(source_urls, target_name, target_settings):
    """Entrypoint for CGW push stage."""
    ret = PushStagedCGW(source_urls, target_name, target_settings)
    pm.register(ret)
    return ret
