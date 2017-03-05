#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © 2017 Taylor C. Richberger <taywee@gmx.com>
# This code is released under the license described in the LICENSE file

from __future__ import division, absolute_import, print_function, unicode_literals
import six

class reader(object):

    """Fixed-table document reader, reading tables with predefined column-sizes"""

    def __init__(self, file, widths, dialect=None, **fmtparams):
        """
        :file: A readable file object that returns lines when iterated upon
        :dialect: A dialect class used to define aspects of the table.
        :widths: An iterable of widths, containing the field sizes of the table.
        :fmtparams: parameters to override the parameters in dialect.
        """
        self._file = file
        self._widths = tuple(widths)
        self._dialect = dialect
        self._fmtparams = fmtparams

    @property
    def file(self):
        return self._file

    @property
    def widths(self):
        return self._widths

    @property
    def dialect(self):
        return self._dialect

    @property
    def fmtparams(self):
        return self._fmtparams
