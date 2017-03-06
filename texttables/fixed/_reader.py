#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © 2017 Taylor C. Richberger <taywee@gmx.com>
# This code is released under the license described in the LICENSE file

from __future__ import division, absolute_import, print_function, unicode_literals
from six.moves import zip
from numbers import Integral

from texttables.dialect import Dialect

class reader(object):

    """Fixed-table table reader, reading tables with predefined column-sizes"""

    def __init__(self, file, widths, dialect=None, fieldnames=None, **fmtparams):
        """
        :file: An iterable object, returning a line with each iteration.
        :widths: An iterable of widths, containing the field sizes of the table.
            Each width may be prefixed with <, >, =, or ^, for alignment through
            the Python format specification, though these prefixes will be ignored
            if they are present.
        :dialect: A dialect class or object used to define aspects of the table.
            The stored dialect is always an instance of Dialect, not the passed-in
            object.
        :fmtparams: parameters to override the parameters in dialect.
        """
        self._file = file
        self._widths = list()
        for width in widths:
            if isinstance(width, Integral):
                self._widths.append(width)
            else:
                swidth = str(width)
                try:
                    width = int(swidth)
                except ValueError:
                    width = int(swidth[1:])
                self._widths.append(width)

        if dialect:
            self.dialect = dialect

        for attribute in dir(self.dialect):
            if '__' not in attribute:
                if attribute in fmtparams:
                    setattr(self._dialect, attribute, fmtparams[attribute])

        self._fieldnames = fieldnames

        self.__foundtop = not self.dialect.top_border
        self.__top = None
        if self.dialect.top_border:
            self.__top = self._rowdelim(self.dialect.top_border)

        self.__header = None
        if self._fieldnames:
            self.__foundheader = True
        else:
            self.__foundheader = not self.dialect.header_delimiter
            if self.dialect.header_delimiter:
                self.__header = self._rowdelim(self.dialect.header_delimiter)

        self.__foundbottom = not self.dialect.bottom_border
        self.__bottom = None
        if self.dialect.bottom_border:
            self.__bottom = self._rowdelim(self.dialect.bottom_border)

        self.__row_delimiter = None
        if self.dialect.row_delimiter:
            self.__row_delimiter = self._rowdelim(self.dialect.row_delimiter)

        self.__found_delimiter = False
        self.__foundrow = False

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self.dialect.bottom_border:
            self.writebottom()

    @property
    def file(self):
        return self._file

    @property
    def widths(self):
        return self._widths

    @property
    def dialect(self):
        return self._dialect

    @dialect.setter
    def dialect(self, value):
        self._dialect = Dialect()
        for attribute in dir(self._dialect):
            if '__' not in attribute:
                setattr(self._dialect, attribute, getattr(value, attribute))

    def _rowdelim(self, delimiter):
        dialect = self.dialect
        delimcontents = list()
        for rawwidth in self._widths:
            swidth = str(rawwidth)
            try:
                width = int(swidth)
            except ValueError:
                width = int(swidth[1:])
            delimcontents.append(delimiter * width)
        delim = ''
        if dialect.left_border:
            delim = dialect.corner_border
        delim += dialect.corner_border.join(delimcontents)
        if dialect.right_border:
            delim += dialect.corner_border
        return delim
