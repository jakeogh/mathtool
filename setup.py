# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup

import fastentrypoints

dependencies = ["click"]

config = {
    "version": "0.1",
    "name": "mathtool",
    "url": "https://github.com/jakeogh/mathtool",
    "license": "ISC",
    "author": "Justin Keogh",
    "author_email": "github.com@v6y.net",
    "description": "Short explination of what it does _here_",
    "long_description": __doc__,
    "packages": find_packages(exclude=["tests"]),
    "package_data": {"mathtool": ["py.typed"]},
    "include_package_data": True,
    "zip_safe": False,
    "platforms": "any",
    "install_requires": dependencies,
}

setup(**config)
