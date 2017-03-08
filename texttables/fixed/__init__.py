#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © 2017 Taylor C. Richberger <taywee@gmx.com>
# This code is released under the license described in the LICENSE file

from __future__ import division, absolute_import, print_function, unicode_literals
import six

__all__ = [
    'reader',
    'writer',
    ]

from ._writer import writer, DictWriter
from ._reader import reader, DictReader
