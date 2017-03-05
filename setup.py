#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © 2016 Absolute Performance Inc <csteam@absolute-performance.com>.
# All rights reserved.
# This is proprietary software.
# No warranty, explicit or implicit, provided.

from __future__ import division, absolute_import, print_function, unicode_literals

from setuptools import setup

from texttables import __author__, __description__, __email__, __license__, __modulename__, __version__, __website__

setup(
    name=__modulename__,
    version=__version__,
    description=__description__,
    author=__author__,
    author_email=__email__,
    url=__website__,
    license=__license__,
    packages=[
        'texttables',
        'texttables.fixed',
        ],
    install_requires=[
        'six',
        ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ]
)
