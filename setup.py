from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read().replace(".. include:: toc.rst\n\n", "")

# The lines below are parsed by `docs/conf.py`.
name = "bfcl"
version = "1.0.0"

setup(
    name=name,
    version=version,
    packages=[name,],
    install_requires=[
        "parts~=1.3",
        "circuit~=0.5"
    ],
    license="MIT",
    url="https://github.com/nthparty/bfcl",
    author="Andrei Lapets",
    author_email="a@lapets.io",
    description="Python library for working with circuit definitions " +\
                "represented using the Bristol Fashion.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
)
