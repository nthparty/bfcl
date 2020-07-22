====
bfcl
====

Bristol Fashion Circuit Library (BFCL) for working with circuit definitions represented using the Bristol Fashion.

|pypi| |travis| |coveralls|

.. |pypi| image:: https://badge.fury.io/py/bfcl.svg
   :target: https://badge.fury.io/py/bfcl
   :alt: PyPI version and link.

.. |travis| image:: https://travis-ci.com/nthparty/bfcl.svg?branch=master
    :target: https://travis-ci.com/nthparty/bfcl

.. |coveralls| image:: https://coveralls.io/repos/github/nthparty/bfcl/badge.svg?branch=master
   :target: https://coveralls.io/github/nthparty/bfcl?branch=master

Purpose
-------
This library includes data structures and associated methods for working with logical circuits typically used in secure multi-party computation (MPC) applications. The data structures follow in their organization the `Bristol Fashion <https://homes.esat.kuleuven.be/~nsmart/MPC/>`_ format, extrapolating and generalizing where necessary in order to support a wider variety of features and operations.

Package Installation and Usage
------------------------------
The package is available on PyPI::

    python -m pip install bfcl

The library can be imported in the usual way::

    import bfcl
    from bfcl import *

Testing and Conventions
-----------------------
All unit tests are executed and their coverage is measured when using `nose <https://nose.readthedocs.io/>`_ (see ``setup.cfg`` for configution details)::

    nosetests

Alternatively, all unit tests are included in the module itself and can be executed using `doctest <https://docs.python.org/3/library/doctest.html>`_::

    python bfcl/bfcl.py -v

Style conventions are enforced using `Pylint <https://www.pylint.org/>`_::

    pylint bfcl

Contributions
-------------
In order to contribute to the source code, open an issue or submit a pull request on the GitHub page for this library.

Versioning
----------
Beginning with version 0.2.0, the version number format for this library and the changes to the library associated with version number increments conform with `Semantic Versioning 2.0.0 <https://semver.org/#semantic-versioning-200>`_.
