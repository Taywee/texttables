#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © 2017 Taylor C. Richberger <taywee@gmx.com>
# This code is released under the license described in the LICENSE file

from __future__ import division, absolute_import, print_function, unicode_literals
from six.moves import zip
from six import Iterator
from numbers import Integral

from texttables.dialect import Dialect
from texttables.errors import ValidationError

class reader(Iterator):

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
        self._iter = iter(file)
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
        self.__finished = False
        self.__bottom = None
        if self.dialect.bottom_border:
            self.__bottom = self._rowdelim(self.dialect.bottom_border)

        self.__row_delimiter = None
        if self.dialect.row_delimiter:
            self.__row_delimiter = self._rowdelim(self.dialect.row_delimiter)

        self.__first_line = True
        self.__foundrow = False

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
        if value is not None:
            for attribute in dir(self._dialect):
                if '__' not in attribute:
                    setattr(self._dialect, attribute, getattr(value, attribute))

    @property
    def fieldnames(self):
        if not self.__foundtop:
            line = next(self._iter).strip('\r\n')
            if self.dialect.strict and line != self.__top:
                raise ValidationError('The first line of the table did not match what the top of the table should be')
            self.__foundtop = True

        if not self._fieldnames:
            line = next(self._iter).strip('\r\n')
            self._fieldnames = self._getline(line)

        if not self.__foundheader:
            line = next(self._iter).strip('\r\n')
            if self.dialect.strict and line != self.__header:
                raise ValidationError("The header of the table wasn't properly delimited")
            self.__foundheader = True

        return self._fieldnames

    def _getline(self, line):
        dialect = self.dialect
        if dialect.left_border:
            if dialect.strict and not line.startswith(dialect.left_border):
                raise ValidationError('row did not have the correct left border')
            line = line[len(dialect.left_border):]
        if dialect.right_border:
            if dialect.strict and not line.endswith(dialect.right_border):
                raise ValidationError('row did not have the correct right border')
            line = line[:-len(dialect.right_border)]

        row = list()

        # Adding delimiter at beginning so that validation doesn't need to be
        # special-cased for the first cell.
        line = dialect.cell_delimiter + line

        for width in self.widths:
            delimiter = line[0:len(dialect.cell_delimiter)]
            if dialect.strict and delimiter != dialect.cell_delimiter:
                raise ValidationError('Cell was not delimited properly')
            line = line[len(dialect.cell_delimiter):]
            contents = line[:width]
            if dialect.strip:
                contents = contents.strip()
            row.append(contents)
            line = line[width:]

        if line:
            raise ValidationError('There was garbage at the end of the input')

        return tuple(row)

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

    def __iter__(self):
        return self

    def __next__(self):
        fieldnames = self.fieldnames

        if self.__finished:
            raise StopIteration

        try:
            line = next(self._iter).strip('\r\n')
            if self.__row_delimiter and not self.__first_line:
                if line != self.__row_delimiter:
                    if line == self.__bottom:
                        self.__foundbottom = True
                        self.__finished = True
                        raise StopIteration
                    if self.dialect.strict:
                        raise ValidationError("This row wasn't properly delimited")
                line = next(self._iter).strip('\r\n')
        except StopIteration:
            # Try to detect if the bottom was found.  If the bottom wasn't
            # found, make sure the bottom doesn't match the row delimiter, which
            # would prevent the bottom from being detected at all
            if self.dialect.strict and not (self.__foundbottom or
                    self.__row_delimiter == self.__bottom):
                raise ValidationError("This table wasn't properly terminated")
            raise StopIteration
        self.__first_line = False
        return self._getline(line)

class DictReader(Iterator):

    """Fixed-table table dictionary reader, reading tables with predefined
    column-sizes"""

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
        self._reader = reader(file, widths, dialect, fieldnames, **fmtparams)
        self._iter = iter(self._reader)

    @property
    def file(self):
        return self._reader.file

    @property
    def widths(self):
        return self._reader.widths

    @property
    def dialect(self):
        return self._reader.dialect

    @dialect.setter
    def dialect(self, value):
        self._reader.dialect = value

    @property
    def fieldnames(self):
        return self._reader.fieldnames

    def __iter__(self):
        return self

    def __next__(self):
        row = next(self._iter)
        return {key: value for key, value in zip(self.fieldnames, row)}
