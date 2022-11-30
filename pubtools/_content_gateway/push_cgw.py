import argparse
import logging
from .push_base import PushBase
from .utils import yaml_parser, validate_data, sort_items, format_cgw_items

LOG = logging.getLogger("pubtools.cgw")
LOG_FORMAT = "%(asctime)s [%(levelname)-8s] %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)


class PushCGW(PushBase):
    """Handle push CGW workflow."""

    def __init__(self, cgw_hostname, cgw_username, cgw_password, cgw_filepath):
        """
        Initialize.

        Args:
            cgw_hostname (str):
                CGW registry URL
            cgw_username (str):
                username for CGW HTTP API
            cgw_password (str):
                password for CGW HTTP API
            cgw_filepath (str):
                filepath of the yaml file
        """

        PushBase.__init__(self, cgw_hostname, cgw_username, cgw_password)
        self.cgw_filepath = cgw_filepath
        self.cgw_items = []

    def cgw_operations(self):
        """
        Initiate the CGW operations such as create, update or delete
        on products, versions and files.
        """

        self.cgw_items = yaml_parser(self.cgw_filepath)
        self.cgw_items = format_cgw_items(self.cgw_items)

        for item in self.cgw_items:
            validate_data(item)
        self.cgw_items = sort_items(self.cgw_items)
        try:
            for item in self.cgw_items:
                if item["type"] == "product":
                    self.process_product(item)
                elif item["type"] == "product_version":
                    self.process_version(item)
                elif item["type"] == "file":
                    self.process_file(item)

            self.make_visible()
            LOG.info("\n All CGW operations are successfully completed...!")
        except Exception as error:
            LOG.exception("Exception occurred during the CGW operation %s" % error)
            LOG.info("Rolling back the partial operation")
            self.rollback_cgw_operation()

            #  raising the occurred Exception as all the exception will get caught in this except block
            #  we want to return full Traceback
            raise error


def main():
    """Entrypoint for CGW Push."""

    parser = argparse.ArgumentParser()
    parser.add_argument("-host", "--CGW_hostname", required=True, metavar="CGW-hostname", help="Hostname of the server")
    parser.add_argument(
        "-u", "--CGW_username", required=True, metavar="CGW-username", help="Username of Content Gateway"
    )
    parser.add_argument("-p", "--CGW_password", metavar="CGW-password", help="Password for Content Gateway")
    parser.add_argument(
        "-f", "--CGW_filepath", required=True, metavar="CGW-filepath", help="File path to read metadata"
    )
    args = parser.parse_args()
    push_cgw = PushCGW(args.CGW_hostname, args.CGW_username, args.CGW_password, args.CGW_filepath)
    push_cgw.cgw_operations()
