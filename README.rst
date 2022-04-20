====
bfcl
====

Bristol Fashion Circuit Library (BFCL) for working with circuit definitions represented using the Bristol Fashion.

|pypi| |actions| |coveralls|

.. |pypi| image:: https://badge.fury.io/py/bfcl.svg
   :target: https://badge.fury.io/py/bfcl
   :alt: PyPI version and link.

.. |actions| image:: https://github.com/nthparty/bfcl/workflows/lint-test-cover-docs/badge.svg
   :target: https://github.com/nthparty/bfcl/actions/workflows/lint-test-cover-docs.yml
   :alt: GitHub Actions status.

.. |coveralls| image:: https://coveralls.io/repos/github/nthparty/bfcl/badge.svg?branch=main
   :target: https://coveralls.io/github/nthparty/bfcl?branch=main

Purpose
-------
This library includes data structures and associated methods for working with logical circuits typically used in secure multi-party computation (MPC) applications. The data structures follow in their organization the `Bristol Fashion <https://homes.esat.kuleuven.be/~nsmart/MPC/>`_ format, extrapolating and generalizing where necessary in order to support a wider variety of features and operations.

Documentation
-------------
.. include:: toc.rst

The documentation can be generated automatically from the source files using `Sphinx <https://www.sphinx-doc.org/>`_::

    cd docs
    python -m pip install -r requirements.txt
    sphinx-apidoc -f -E --templatedir=_templates -o _source .. ../setup.py && make html

Package Installation and Usage
------------------------------
The package is available on PyPI::

    python -m pip install bfcl

The library can be imported in the usual way::

    import bfcl
    from bfcl import *

Testing and Conventions
-----------------------
All unit tests are executed and their coverage is measured when using `pytest <https://docs.pytest.org/>`_ (see ``setup.cfg`` for configuration details)::

    python -m pip install pytest pytest-cov
    python -m pytest

Alternatively, all unit tests are included in the module itself and can be executed using `doctest <https://docs.python.org/3/library/doctest.html>`_::

    python bfcl/bfcl.py -v

Style conventions are enforced using `Pylint <https://www.pylint.org/>`_::

    python -m pip install pylint
    python -m pylint bfcl

Contributions
-------------
In order to contribute to the source code, open an issue or submit a pull request on the GitHub page for this library.

Versioning
----------
Beginning with version 0.2.0, the version number format for this library and the changes to the library associated with version number increments conform with `Semantic Versioning 2.0.0 <https://semver.org/#semantic-versioning-200>`_.

Publishing
----------
This library can be published as a `package on PyPI <https://pypi.org/project/bfcl/>`_ by a package maintainer. Install the `wheel <https://pypi.org/project/wheel/>`_ package, remove any old build/distribution files, and package the source into a distribution archive::

    python -m pip install wheel
    rm -rf dist *.egg-info
    python setup.py sdist bdist_wheel

Next, install the `twine <https://pypi.org/project/twine/>`_ package and upload the package distribution archive to PyPI::

    python -m pip install twine
    python -m twine upload dist/*
