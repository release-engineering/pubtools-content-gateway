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
The YAML file can consist details of Products, Versions and Files.

YAML file formats
********************************
The user can pass a single or multiple records of product, version and file in a single YAML file.
A typical YAML format for Product, version and file looks like this:

.. code-block::

    # YAML file formats for Product
    - type: product                                             # MANDATORY
      state: create                                             # MANDATORY
      metadata:
        name: "Test Product"                                    # MANDATORY
        productCode: "TestProduct"                              # MANDATORY
        homepage: "https://test.com/"                           # OPTIONAL
        downloadpage: "https://test.com/"                       # OPTIONAL
        thankYouPage: "https://test.com/"                       # OPTIONAL
        eloquaCode: "NOT_SET"                                   # OPTIONAL
        featuredArtifactType: "Server"                          # OPTIONAL
        thankYouTimeout: 5                                      # OPTIONAL

    # YAML file formats for Version
    - type: product_version                                     # MANDATORY
      state: create                                             # MANDATORY
      metadata:
        productName: "Test Product"                             # MANDATORY
        productCode: "TestProduct"                              # MANDATORY
        versionName: "TestProductVersion"                       # MANDATORY
        ga: true                                                # OPTIONAL
        masterProductVersion: null                              # OPTIONAL
        termsAndConditions: "Anonymous Download"                # MANDATORY
        trackingDisabled: true                                  # OPTIONAL
        hidden: true                                            # OPTIONAL
        invisible: true                                         # OPTIONAL

    # YAML file formats for File
    - type: file                                                # MANDATORY
      state: create                                             # MANDATORY
      metadata:
        type: "FILE"                                            # MANDATORY
        productName: "Test Product"                             # MANDATORY
        productCode: "TestProduct"                              # MANDATORY
        productVersionName: "TestProductVersion"                # MANDATORY
        description: "Test description"                         # MANDATORY
        label: "Release Info"                                   # MANDATORY
        order: 0                                                # OPTIONAL
        hidden: false                                           # OPTIONAL
        downloadURL: "/content/origin/files/TestProduct/"       # MANDATORY
        shortURL: "/test-1/example-v4/testing/"                 # MANDATORY
        differentProductThankYouPage: "Any Thank You Page"      # OPTIONAL

    ... # many other records


To know more content gateway operations about add, update and delete please visit :doc:`push_base`.