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

    def __init__(self, file, widths, dialect=None, **fmtparams):
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
        self._dialect = Dialect()
        for attribute in dir(self._dialect):
            if '__' not in attribute:
                if attribute in fmtparams:
                    setattr(self._dialect, field, fmtparams[attribute])
                else:
                    if dialect is not None:
                        setattr(self._dialect, attribute, getattr(dialect, attribute))

        self.__foundtop = not self._dialect.top_border
        self.__foundheader = not self._dialect.header_delimiter
        self.__foundbottom = not self._dialect.bottom_border
        self.__founddelim = False
        self.__foundrow = False

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self._dialect.bottom_border:
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

    def writerow(self, row):
        dialect = self._dialect
        if self.__wroteheader:
            if (dialect.header_delimiter is not None
                and dialect.corner_border is not None
                ):
                self._file.write(self._rowdelim(dialect.header_delimiter))
                self._file.write(dialect.lineterminator)
        elif self.__wroterow:
            if (dialect.row_delimiter is not None
                and dialect.corner_border is not None
                ):
                self._file.write(self._rowdelim(dialect.row_delimiter))
                self._file.write(dialect.lineterminator)

        self._file.write(self._row(row))
        self._file.write(dialect.lineterminator)

        self.__wroteheader = False
        self.__wroterow = True

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

    def writeheader(self, row):
        self.writerow(row)
        self.__wroteheader = True

    def writetop(self):
        dialect = self._dialect
        self._file.write(self._rowdelim(dialect.top_border))
        self._file.write(dialect.lineterminator)

    def writebottom(self):
        dialect = self._dialect
        self._file.write(self._rowdelim(dialect.bottom_border))
        self._file.write(dialect.lineterminator)

class DictWriter(object):
    """Fixed-table document writer, writing tables with predefined column-sizes
    and names"""

    def __init__(self, file, fieldnames, widths, dialect=None, **fmtparams):
        """
        :file: A writable file object with a ``write`` method
        :fieldnames: A sequence of field names
        :dialect: A dialect class used to define aspects of the table.
        :widths: An iterable of widths, containing the field sizes of the table.
         Each width may be prefixed with <, >, =, or ^, for alignment through
         the Python format specification.
        :fmtparams: parameters to override the parameters in dialect.
        """

        self._writer = writer(file, widths, dialect, **fmtparams)
        self._fieldnames = fieldnames

    def __enter__(self):
        self._writer.__enter__()
        return self

    def __exit__(self, type, value, traceback):
        self._writer.__exit__(type, value, traceback)
        return self

    @property
    def file(self):
        return self._writer.file

    @property
    def widths(self):
        return self._writer.widths

    @property
    def dialect(self):
        return self._writer.dialect

    @property
    def fieldnames(self):
        return self._fieldnames

    @fieldnames.setter
    def fieldnames(self, value):
        self._fieldnames = value

    def writeheader(self):
        self._writer.writeheader(self._fieldnames)

    def writerow(self, row):
        self._writer.writerow(row[field] for field in self._fieldnames)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

    def writetop(self):
        self._writer.writetop()

    def writebottom(self):
        self._writer.writebottom()
