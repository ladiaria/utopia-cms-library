# -*- coding: utf-8 -*-
"""
A book management app for utopia-cms
2022,2026 Utopia.
"""
import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

from utopia_cms_library import DIST_NAME, DESCRIPTION  # noqa

setup(
    name=DIST_NAME,
    version="0.1.1",
    python_requires=">=3.10.6,<=3.12.8",
    packages=find_packages(),
    include_package_data=True,
    description=DESCRIPTION,
    long_description=README,
    author='utopia',
    author_email='it@ladiaria.com.uy',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
