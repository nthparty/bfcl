from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="bfcl",
    version="0.3.0",
    packages=["bfcl",],
    install_requires=["parts>=0.2.1", "circuit>=0.3.0",],
    license="MIT",
    url="https://github.com/nthparty/bfcl",
    author="Andrei Lapets",
    author_email="a@lapets.io",
    description="Python library for working with circuit definitions " +\
                "represented using the Bristol Fashion.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    test_suite="nose.collector",
    tests_require=["nose"],
)
