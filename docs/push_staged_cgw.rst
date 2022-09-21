Push Staged CGW Module
====================================================

The push-staged-cgw (:doc:`push_staged_cgw`) is a target entrypoint for Push Staged which will be invoked through Red Hat's internal service called `rcm-pub`.

All the user credentials will be received through the argument ``target_settings`` consisting of `server_name`, `username` and `password`.
It shares the same YAML file structure except `downloadURL` user need to pass `pushItemPath`.

.. automodule:: pubtools._content_gateway.push_staged_cgw
   :members:
   :show-inheritance:
   :noindex:


YAML file formats
***********************
The user can pass a single or multiple records of product, version and files in a single YAML file.
A typical YAML format for Product, version and file looks like this:

.. code-block::

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
        pushItemPath: "/content/origin/files/TestProduct/"      # MANDATORY
        shortURL: "/test-1/example-v4/testing/"                 # MANDATORY
        differentProductThankYouPage: "Any Thank You Page"      # OPTIONAL

    ... # other records