#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Author: Leann Mak
# Email: leannmak@139.com
# (C) 2018
#
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    print ("lotus now needs setuptools in order to build. Install it using "
           "your package manager (usually python-setuptools) or via pip "
           "(pip install setuptools).")
    sys.exit(1)

# specify installation requirements
with open("requirements.txt") as requirements_file:
    install_requires = requirements_file.read().splitlines()
    if not install_requires:
        print ("Unable to read requirements from the requirements.txt file"
               "That indicates this copy of the source code is incomplete.")
        sys.exit(2)

# specify test requirements
with open("test/requirements.txt") as test_requirements_file:
    test_requires = test_requirements_file.read().splitlines()
    if not test_requires:
        print ("Unable to read requirements from the test/requirements.txt file"
               "That indicates this copy of the source code is incomplete.")
        sys.exit(3)

setup(
    name="lotus",
    version="0.1.0",
    description="python api for common open source tools",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 2.7",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent"
    ],
    keywords="ansible disconf etcd minio",
    author="leannmak",
    author_email="leannmak@139.com",
    url="",
    license="NO LICENSE",
    package_dir={"": "lib"},
    packages=find_packages("lib"),
    include_package_data=True,
    zip_safe=False,
    platforms="pypy",
    install_requires=install_requires,
    tests_require=test_requires,
    test_suite="nose.collector",
    )
