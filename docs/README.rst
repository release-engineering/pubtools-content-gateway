===============
    Overview
===============

Set of scripts used for operating with the Content Gateway (CGW) service

Details
============

content-gateway is a library used for performing various content workflows related work. The library is utilized by Red Hat's internal tooling or release engineers for pushing and managing the contents of products, versions and files on the content gateway server.

Some scripts support a CLI invocation and may be utilized by end-users directly. These are mostly content management operations and are expected to be performed ad-hoc and on a need-to basis. Other scripts can only be invoked programmatically from a different Python code. These are generally a part of standard content workflows and are expected to be invoked by internal Red Hat tooling.

The internal service which utilizes this library is called `rcm-pub <https://pub.devel.redhat.com/pub/docs/usage.html>`_ (hence pubtools in the name).

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

