Entrypoints reference
=====================

Reference to entrypoints provided by pubtools content gateway (CGW). The entrypoints can be invoked by using a CLI, or programmatically with the provided master-level function.



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
***********************

A typical invocation to push a metadata would look like this:

.. code-block::

  push-cgw-metadata \
    --CGW_hostname https://content-gateway/example.com \
    --CGW_username admin \
    --CGW_password XXXXX \
    --CGW_filepath docs/cgw/cgw_push.yaml

  or

  push-cgw-metadata -host https://content-gateway/example.com \
                    -p XXXXX \
                    -u admin \
                    -f full_path_to_yaml_file/cgw_push.yaml


.. _YAML format:

YAML file entities formats
*****************************
One can Add, Update and Delete the contents from CGW.
The YAML file can consist list of Products, Versions and Files


Product
---------------
The highest in the hierarchy is a product. It contains significant details like `name`, `code`, `downloadpage` etc. (see below in YAML format)

Version
---------------
Each product can have multiple product versions. Product version groups files based on when they were released. Product version is identified by its name. The version name must be unique within the product scope, however there can be other product versions with the same name in a different product scope.

Besides a name the product version contains release date field, that is used in ordering product versions. If you set future date, the files will not appear in download tables until the release date.  It is also possible to add information whether the product version is the final version or early access.

If you mark the product version as "hidden", all the files in the version will not be displayed and it will not be possible to download them. If the product version is marked as invisible, the files can be downloaded if someone knows the right URL, but the links will not appear in the download tables.

File
---------------
Each product version may contain one or more files. The file is identified by its path on access.cdn

A typical linear YAML format for Product, version and file looks like this:

.. code-block::

    # YAML file formats for Product
    - type: product                                             # MANDATORY
      action: create                                            # MANDATORY
      metadata:
        name: "Test Product"                                    # MANDATORY
        productCode: "TestProduct"                              # MANDATORY
        homepage: "https://test.com/"                           # OPTIONAL
        downloadpage: "https://test.com/"                       # OPTIONAL
        thankYouPage: "https://test.com/"                       # OPTIONAL
        eloquaCode: "NOT_SET"                                   # MANDATORY
        featuredArtifactType: "Server"                          # OPTIONAL
        thankYouTimeout: 5                                      # OPTIONAL

    # YAML file formats for Version
    - type: product_version                                     # MANDATORY
      action: create                                            # MANDATORY
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
      action: create                                            # MANDATORY
      metadata:
        type: "FILE"                                            # MANDATORY
        productName: "Test Product"                             # MANDATORY
        productCode: "TestProduct"                              # MANDATORY
        productVersionName: "TestProductVersion"                # MANDATORY
        description: "Test description"                         # OPTIONAL
        label: "Release Info"                                   # OPTIONAL
        order: 0                                                # OPTIONAL
        hidden: false                                           # OPTIONAL
        downloadURL: "/content/origin/files/TestProduct/"       # MANDATORY
        shortURL: "/test-1/example-v4/testing/"                 # OPTIONAL
        differentProductThankYouPage: "Any Thank You Page"      # OPTIONAL

    ... # other records


The YAML data can also be passed in nested structure like:-

.. code-block::

    # nested yaml data structure
    - product:
        action: create
        name: Product_Name_1
        productCode: Product_code_1
        homepage: https://fake.example.com/products/fake-containers/overview/
        downloadpage: https://fake.example.com/products/fake-containers/download/
        thankYouPage: https://example.com/
        thankYouTimeout: 5
        eloquaCode: fakeCODE9999

        releases:
          - versionName: 3.4.0
            masterProductVersion: null
            ga: true
            hidden: false
            invisible: false
            termsAndConditions: Anonymous Download

            files:
              - downloadURL: "/content/origin/files/AnsibleNewTest_1/"

              - downloadURL: "/content/fake/files/AnsibleNewTest_2/"
                # other metadata

          - versionName: 3.4.1
            termsAndConditions: Anonymous Download
            # other metadata

            files:
              - downloadURL: "/content/fake/files/AnsibleNewTest_3/"
                # other metadata

    - product:
        action: create
        name: Product_Name_2
        productCode: Product_code_2
        eloquaCode: FAKECODE1234

        releases:
          - versionName: 3.4.4
            termsAndConditions: Anonymous Download

            files:
              - downloadURL: "/content/origin/files/AnsibleNewTest_4/"

To know more content gateway operations about add, update and delete please visit :doc:`push_base`.

.. note::
    To update any record you can either pass the exact id of the product, version and file or
    the CGW will automatically fetch the id of the record if it is not mentioned in the metadata.

    ID is mandatory to update the following fields:
        #. name of product
        #. productCode
        #. versionName
        #. downloadURL
        #. pushItemPath

Benefit of using Linear YAML structure
---------------------------------------------
Linear YAML structure gives us the flexibility to perform operation on a single
record at a time without being bothered by its subsequent or parent records.
We can update multiple independent records by using linear structure. Refer examples in next section.

Operation on a single record
-----------------------------
One can create, update and delete multiple records with the nested YAML structure at a time,
but if we want to perform a single operation, especially on the child records then we must use
linear/sequential YAML structure. Because it gives us the flexibility to define data for only a single
record without being bothered by its subsequent or parent records.

Examples
___________
Creating, updating and deleting a single or independent child records can be
easily achieved by using linear structure. Linear YAML file structure also allow
us to perform multiple distinct operations on individual records.

Please refer the below example:-
.. code-block::

    # Create request for a single file entry of a product and version
    - type: file
      action: create
      metadata:
        type: "FILE"
        productName: "Test Product"
        productCode: "TestProduct"
        productVersionName: "TestProductVersion"
        description: "Test description"
        label: "Release Info"
        order: 0
        hidden: false
        downloadURL: "/content/origin/files/TestProduct/"
        shortURL: "/test-1/example-v4/testing/"
        differentProductThankYouPage: "Any Thank You Page"

    # Update request for a single file entry of a version
    - type: product_version
      action: update
      metadata:
        productName: "Test Product"
        productCode: "TestProduct"
        versionName: "TestProductVersion"
        ga: true
        termsAndConditions: "Anonymous Download"
        hidden: true

    # Delete request for an independent Product
    # the product must not have any child associated with it during deletion
    - type: product
      action: delete
      metadata:
        name: "AnsibleTest Product"
        productCode: "Ansible TestProduct"

    ... # other records


push-staged-cgw
........................

The push-staged-cgw (:doc:`push_staged_cgw`) is a target entrypoint for Push Staged which will be invoked through Red Hat's internal service called `rcm-pub`.

All the user credentials will be received through the argument ``target_settings`` consisting of `server_name`, `username` and `password`.
It shares the same YAML file structure except `downloadURL` user need to pass `pushItemPath`.


YAML file formats
************************
The user can pass a single or multiple records of product, version and file in a single YAML file.
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
        label: "Release Info"                                   # OPTIONAL
        order: 0                                                # OPTIONAL
        hidden: false                                           # OPTIONAL
        pushItemPath: "/content/origin/files/TestProduct/"      # MANDATORY
        shortURL: "/test-1/example-v4/testing/"                 # OPTIONAL
        differentProductThankYouPage: "Any Thank You Page"      # OPTIONAL

    ... # other records

.. note::
    This data can also be passed in nested structure same as defined above.