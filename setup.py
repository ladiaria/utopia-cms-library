# -*- coding: utf-8 -*-
"""
A book management app for utopia-cms
2022, utopia.
"""
from __future__ import unicode_literals

import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='utopia-cms-library',
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    description="A book management app for utopia-cms",
    long_description=README,
    author='utopia',
    author_email='it@ladiaria.com.uy',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7.11',
    ],
)

