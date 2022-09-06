# from utils import yaml_parser
# import json


# def ret_it():
#     path = "/Users/jalam/Workprofile/pubtools-content-gateway/tests/test_data/test_cgw_push_staged.yaml"
#     # print(yaml_parser(path))
#     print(json.dumps(yaml_parser(path), sort_keys=True, indent=4))
# ret_it()
# class Cal:
#
#     def client_methods(self, key, method_parameters):
#         methods_dict = {
#             'plus': self.add,
#             'min': self.sub,
#             'inc': self.inc,
#             'disp': self.show
#         }
#         x = methods_dict[key](*method_parameters)
#         print(x)
#     def add(self, x,y):
#         return x+y
#
#     def sub(self, x,y,z):
#         # x, y = args
#         return z-(x+y)
#
#     def inc(self, x):
#         # x = args[0]
#         x += 1
#         return x
#
#     def show(self):
#         print("I am here to display")
#
# c = Cal()
# c.client_methods('disp', [])


# def api_methods_call(self, key, parameters):
#     response = []
#     if not self.debug:
#         api_methods = {
#             'get_products': self.cgw_client.get_products,
#             'create_product': self.cgw_client.create_product,
#             'update_product': self.cgw_client.update_product,
#             'delete_product': self.cgw_client.delete_product,
#
#             'get_versions': self.cgw_client.get_versions,
#             'create_version': self.cgw_client.create_version,
#             'update_version': self.cgw_client.update_version,
#             'delete_version': self.cgw_client.delete_version,
#
#             'get_files': self.cgw_client.get_files,
#             'create_file': self.cgw_client.create_file,
#             'update_file': self.cgw_client.update_file,
#             'delete_file': self.cgw_client.delete_file,
#         }
#         response = api_methods[key](*parameters)
