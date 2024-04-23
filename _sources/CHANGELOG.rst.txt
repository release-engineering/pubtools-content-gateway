ChangeLog
=========

0.5.2 (2024-04-23)
------------------
* adjust schema for Pub pushes without pushItemPath

0.5.1 (2023-07-10)
------------------
* Fix release workflow

0.5.0 (2023-07-10)
------------------
* Support RAW content push
* Bump python version to 3.9
* Initialize logger at run time

0.4.0 (2023-01-31)
------------------
* Read md5sum from push items processed by pulp
* Dropped python2 support


0.3.0 (2022-11-16)
------------------

* Pubtools CGW can support nested structure of data in YAML file
* Changed the YAML field `state` to `action` to denote more appropriate operation
* File `order` in YAML will be auto incremented by 10 for nested data structure
* Updated documentation


0.2.3 (2022-11-24)
------------------

* Get push item size when proceses


0.2.2 (2022-11-10)
------------------

* Additional integration fixes

0.2.1 (2022-11-07)
------------------

* Fixed entry point loading for push-staged

0.2.0 (2022-11-07)
------------------

* Integration of pubtools push-staged
* Added documentation


0.1.0 (2022-09-15)
------------------

* Initial release.
* Added push-cgw-metadata entrypoint
* Added authentication for CGW
* APIs for CGW calls
* Added workflow operations for product, versions and file
