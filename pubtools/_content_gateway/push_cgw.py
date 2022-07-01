import argparse
from .push_base import PushBase
from .utils import yaml_parser


class PushCGW(PushBase):
    def __init__(self, cgw_hostname, cgw_username, cgw_password, cgw_filepath):
        PushBase.__init__(self, cgw_hostname, cgw_username, cgw_password)
        self.cgw_filepath = cgw_filepath

    def cgw_operations(self):
        # parsing, validating and sorting yaml file data
        cgw_items = yaml_parser(self.cgw_filepath)
        # Creating product mapping to get the product_id with name and productCode
        cgw_products = self.cgw_client.get_products()
        for data in cgw_products:
            self.product_mapping[(data['name'], data['productCode'])] = data['id']
        for item in cgw_items:
            if item['type'] == 'product':
                self.process_product(item)
            elif item['type'] == 'product_version':
                self._create_product_version_mapping(item.get('metadata')['productName'],
                                                     item.get('metadata')['productCode'])
                self.process_version(item)
            elif item['type'] == 'file':
                self.process_file(item, False)


def main():
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
