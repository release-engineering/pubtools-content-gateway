===============
    Overview
===============

Set of scripts used for operating with the Content Gateway (CGW) service

Details
============

content-gateway is a library used for performing various content workflows related work. The library is utilized by Red Hat's internal tooling or release engineers for pushing and managing the contents of products, versions and files on the content gateway server.

The internal service which utilizes this library is called `rcm-pub`.

--------------------------------


Requirements
============

- Python 2.6+
- Python 3.5+

--------------------------------


Setup
=====

::

  $ pip install -r requirements.txt
  $ pip install .
  or
  $ python setup.py install

-----------------------------


Steps to use
============

1) Setup
2) Create a YAML file with required entries for Products, Versions or Files (See :doc:`entrypoints_reference` for more details)
3) Use *push-cgw-metadata* entrypoint to do the push operation


Example
--------------

Example YAML file
....................
In this example we are creating one product.
We have created this `cgw_example.yaml` file with the following content

.. code-block::

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
        thankYouTimeout: 5


Use of entrypoint
....................
``push-cgw-metadata`` (:doc:`entrypoints_reference`) entrypoint needs to be invoked to do the pushes.
The below is an example of its invocation

.. code-block::

  push-cgw-metadata -host https://content-gateway/example.com \
                    -p XXXXX \
                    -u username \
                    -f full_path_to_yaml_file/cgw_example.yaml

  2022-09-21 12:29:01,508 [INFO    ] Data validation successful for product: TestProduct
  2022-09-21 12:29:01,508 [DEBUG   ] Fetching for product_id of product_name:- Test Product and product_code:- TestProduct

  2022-09-21 12:29:01,515 [DEBUG   ] Starting new HTTPS connection (1): content-gateway/example.com:443
  2022-09-21 12:29:03,183 [DEBUG   ] https://content-gateway/example.com:443 "GET /content-gateway/rest/admin/products HTTP/1.1" 200 None
  2022-09-21 12:29:03,808 [DEBUG   ] https://content-gateway/example.com:443 "PUT /content-gateway/rest/admin/products/ HTTP/1.1" 201 7
  2022-09-21 12:29:03,808 [INFO    ] Created a new product with product_id:- 4009801

  2022-09-21 12:29:03,808 [DEBUG   ] Updating the invisible attribute of the created records
  2022-09-21 12:29:03,808 [DEBUG   ] Enabling the created records if required

  2022-09-21 12:29:03,808 [INFO    ]
  All CGW operations are successfully completed...!

We can see in the logs that the product is created with some ID.