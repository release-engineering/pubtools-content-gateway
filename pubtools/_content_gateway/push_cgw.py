import argparse
from .push_base import PushBase
from .utils import yaml_parser, validate_data, sort_items


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
        # Creating product mapping to get the product_id with name and productCode
        for item in self.cgw_items:
            validate_data(item)
        self.cgw_items = sort_items(self.cgw_items)
        for item in self.cgw_items:
            if item['type'] == 'product':
                self.process_product(item)
            elif item['type'] == 'product_version':
                self.process_version(item)
            elif item['type'] == 'file':
                self.process_file(item)


def main():
    """Entrypoint for CGW Push."""

    parser = argparse.ArgumentParser()
    parser.add_argument("-host", "--CGW_hostname",
                        required=True,
                        metavar="CGW-hostname",
                        help="Hostname of the server")
    parser.add_argument("-u", "--CGW_username",
                        required=True,
                        metavar="CGW-username",
                        help="Username of Content Gateway")
    # TODO: Read password form the environment variable if it's set
    parser.add_argument("-p", "--CGW_password",
                        metavar="CGW-password",
                        help="Password for Content Gateway")
    parser.add_argument("-f", "--CGW_filepath",
                        required=True,
                        metavar="CGW-filepath",
                        help="File path to read metadata")
    args = parser.parse_args()
    push_cgw = PushCGW(args.CGW_hostname, args.CGW_username, args.CGW_password, args.CGW_filepath)
    push_cgw.cgw_operations()
