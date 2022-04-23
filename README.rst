====
bfcl
====

Bristol Fashion Circuit Library (BFCL) for working with circuit definitions represented using the Bristol Fashion.

|pypi| |readthedocs| |actions| |coveralls|

.. |pypi| image:: https://badge.fury.io/py/bfcl.svg
   :target: https://badge.fury.io/py/bfcl
   :alt: PyPI version and link.

.. |readthedocs| image:: https://readthedocs.org/projects/bfcl/badge/?version=latest
   :target: https://bfcl.readthedocs.io/en/latest/?badge=latest
   :alt: Read the Docs documentation status.

.. |actions| image:: https://github.com/nthparty/bfcl/workflows/lint-test-cover-docs/badge.svg
   :target: https://github.com/nthparty/bfcl/actions/workflows/lint-test-cover-docs.yml
   :alt: GitHub Actions status.

.. |coveralls| image:: https://coveralls.io/repos/github/nthparty/bfcl/badge.svg?branch=main
   :target: https://coveralls.io/github/nthparty/bfcl?branch=main
   :alt: Coveralls test coverage summary.

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

This library makes it possible to parse a circuit definition that conforms to the Bristol Fashion syntax::

    >>> ss = ['7 36', '2 4 4', '1 1']
    >>> ss += ['2 1 0 1 15 AND', '2 1 2 3 16 AND']
    >>> ss += ['2 1 15 16 8 AND', '2 1 4 5 22 AND']
    >>> ss += ['2 1 6 7 23 AND', '2 1 22 23 9 AND']
    >>> ss += ['2 1 8 9 35 AND']
    >>> c = circuit('\n'.join(ss))

A string representation that conforms to the Bristol Fashion syntax can be emitted::

    >>> for line in c.emit().split('\n'):
	...     print(line)
	...
	7 36
	2 4 4
	1 1
	2 1 0 1 15 AND
	2 1 2 3 16 AND
	2 1 15 16 8 AND
	2 1 4 5 22 AND
	2 1 6 7 23 AND
	2 1 22 23 9 AND
	2 1 8 9 35 AND

It is possible to evaluate a circuit on a sequence of input bit vectors. The circuit defined in the example above takes two 4-bit input vectors and returns the logical conjunction of all the bits. In the example below, it is evaluated on a few pairs of input bit vectors. The result is organized into a list of output bit vectors according to the original circuit definition (in the example below, the result consists of only a single output bit vector that contains a single bit)::

	>>> c.evaluate([[1, 0, 1, 1], [1, 1, 1, 0]])
	[[0]]
	>>> c.evaluate([[1, 1, 1, 1], [1, 1, 1, 1]])
	[[1]]

As an alternative to using a string representation to define a circuit, it is also possible to construct a circuit using the `circuit <https://pypi.org/project/circuit/>`_ library. In the example below, the constructor for the ``circuit`` class found in the `bfcl <https://pypi.org/project/bfcl/>`_ library is applied to an object built using the classes and methods exported by the `circuit <https://pypi.org/project/circuit/>`_ library (note the use of a synonym to avoid a conflict with the ``circuit`` class defined in the `bfcl <https://pypi.org/project/bfcl/>`_ library)::

	>>> import circuit as circuit_
	>>> c = circuit_.circuit()
	>>> g0 = c.gate(circuit_.op.id_, is_input=True)
	>>> g1 = c.gate(circuit_.op.id_, is_input=True)
	>>> g2 = c.gate(circuit_.op.and_, [g0, g1])
	>>> g3 = c.gate(circuit_.op.id_, [g2], is_output=True)
	>>> circuit(c).emit().split('\n')
	['2 4', '1 2', '1 1', '2 1 0 1 2 AND', '1 1 2 3 LID']

Documentation
-------------
.. include:: toc.rst

The documentation can be generated automatically from the source files using `Sphinx <https://www.sphinx-doc.org/>`_::

    cd docs
    python -m pip install -r requirements.txt
    sphinx-apidoc -f -E --templatedir=_templates -o _source .. ../setup.py && make html

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
