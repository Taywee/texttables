#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © 2017 Taylor C. Richberger <taywee@gmx.com>
# This code is released under the license described in the LICENSE file

from __future__ import division, absolute_import, print_function, unicode_literals
from six import iteritems
from six.moves import zip

from texttables.dialect import Dialect, _DIALECTFIELDS

class writer(object):

    """Fixed-table document writer, writing tables with predefined column-sizes"""

    def __init__(self, file, widths, dialect=None, **fmtparams):
        """
        :file: A writable file object with a ``write`` method
        :dialect: A dialect class used to define aspects of the table.
        :widths: An iterable of widths, containing the field sizes of the table.
         Each width may be prefixed with <, >, =, or ^, for alignment through
         the Python format specification.
        :fmtparams: parameters to override the parameters in dialect.
        """
        self._file = file
        self._widths = tuple(widths)
        self._dialect = Dialect()
        for field in _DIALECTFIELDS:
            if field in fmtparams:
                setattr(self._dialect, field, fmtparams[field])
            else:
                setattr(self._dialect, field, getattr(dialect, field))

        self.__wroterow = False
        self.__wroteheader = False

    def __enter__(self):
        self.writetop()

    def __exit__(self, type, value, traceback):
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

    def _row(self, row):
        dialect = self._dialect
        contents = list()
        for cell, rawwidth in zip(row, self._widths):
            swidth = str(rawwidth)
            alignment = '<'
            try:
                width = int(swidth)
            except ValueError:
                alignment = swidth[0]
                width = int(swidth[1:])
            contents.append('{content!s:{alignment}{width}.{width}s}'.format(
                content=cell,
                alignment=alignment,
                width=width))
        row = ''
        if dialect.left_border:
            row = dialect.left_border
        row += dialect.cell_delimiter.join(contents)
        if dialect.right_border:
            row += dialect.right_border
        return row

    def _rowdelim(self, delimiter):
        dialect = self._dialect
        delimcontents = list()
        for width in self._widths:
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

    def writerow(self, row):
        if (self.__wroterow
            and dialect.row_delimiter is not None
            and dialect.corner_border is not None
            ):
            prerow = self._rowdelim(dialect.header_delimiter if self.__wroteheader else dialect.row_delimiter)
            self.__wroteheader = False
        if prerow is not None:
            self._file.write(prerow)
            self._file.write(dialect.lineterminator)

        self._file.write(self._row(row))
        self._file.write(dialect.lineterminator)
        self.__wroterow = True

    def writeheader(self, row):
        self.writerow(row)
        self.__wroteheader = True

    def writetop(self):
        self._file.write(self._rowdelim(dialect.top_border))
        self._file.write(dialect.lineterminator)

    def writebottom(self):
        self._file.write(self._rowdelim(dialect.bottom_border))
        self._file.write(dialect.lineterminator)

