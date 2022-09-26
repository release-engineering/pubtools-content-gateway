Push CGW Module
========================

Content Gateway (CGW) is a library used for performing various content workflows related work. The ``push-cgw-metadata`` entrypoint will be utilized by users for pushing and managing the contents of products, versions and files on the content gateway server.

.. automodule:: pubtools._content_gateway.push_cgw
   :members:
   :special-members:
   :show-inheritance:
   :noindex:

The main() method will be invoked when entrypoint is called and it will pass all required received credentials to the ``PushCGW`` class for the CGW operations.

CGW environment
........................

.. code-block::

  usage: push-cgw-metadata   [-h] -host CGW-hostname -u CGW-username [-p CGW-password] -f CGW-filepath
                             optional arguments:
                                  -h, --help            show this help message and exit

                                  -host CGW-hostname, --CGW_hostname CGW-hostname
                                                        Hostname of the server

                                  -u CGW-username, --CGW_username CGW-username
                                                        Username of Content Gateway

                                  -p CGW-password, --CGW_password CGW-password
                                                        Password for Content Gateway

                                  -f CGW-filepath, --CGW_filepath CGW-filepath
                                                        File path to read metadata


``--host`` or ``--CGW_hostname``
  Hostname of the server

``-u`` or ``--CGW_username``
  Username of Content Gateway

``-P`` or ``--CGW_password``
  Password for Content Gateway

``-f`` or ``--CGW_filepath``
  File path to read metadata


Example
........................

A typical invocation to push a metadata would look like this:

.. code-block::

  push-cgw-metadata \
    --CGW_hostname https://content-gateway/example.com \
    --CGW_username admin \
    --CGW_password XXXXX \
    --CGW_filepath Users/example/cgw/cgw_push.yaml


YAML file formats
........................
One can Add, Update and Delete the contents from CGW
The YAML file can consist details of Products, Versions and Files. Please refer :ref:`YAML format` for more details.
