#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © 2017 Taylor C. Richberger <taywee@gmx.com>
# This code is released under the license described in the LICENSE file

from __future__ import division, absolute_import, print_function, unicode_literals
from six.moves import zip
from texttables.dialect import Dialect

class writer(object):

    """Fixed-table document writer, writing tables with predefined column-sizes.
    The :class:`texttables.Dialect` class is used to configure how this writes
    tables.  This works as a context manager, in which case :meth:`writetop` and
    :meth:`writebottom` will be called automatically."""


    def __init__(self, file, widths, dialect=None, **fmtparams):
        """
        :param file: A writable file object with a ``write`` method
        :param widths: An iterable of widths, containing the field sizes of the table.
            Each width may be prefixed with <, >, =, or ^, for alignment through
            the Python format specification.
        :param dialect: A dialect class or object used to define aspects of the
            table.  The stored dialect is always an instance of
            :class:`texttables.Dialect`, not necessarily the passed-in object.
            All the attributes of Dialect are grabbed from this object using
            getattr.
        :param fmtparams: parameters to override the parameters in
            :obj:`dialect`.
        """
        self._file = file
        self._widths = tuple(widths)

        self.dialect = dialect

        for attribute in dir(self.dialect):
            if '__' not in attribute:
                if attribute in fmtparams:
                    setattr(self._dialect, attribute, fmtparams[attribute])

        self.__wroterow = False
        self.__wroteheader = False

    def __enter__(self):
        if self.dialect.top_border:
            self.writetop()
        return self

    def __exit__(self, type, value, traceback):
        if self.dialect.bottom_border:
            self.writebottom()

    @property
    def file(self):
        '''The file object that was passed in to the constructor.  It is not
        safe to change this object until you are finished using the class'''
        return self._file

    @property
    def widths(self):
        '''The widths that were passed into the constructor, as a tuple.'''
        return self._widths

    @property
    def dialect(self):
        '''The :class:`texttables.Dialect` constructed from the passed-in
        dialect.  This is always unique, and is not the same object that is
        passed in.  Assigning to this will also likewise construct a new
        :class:`texttables.Dialect`, not simply assign the attribute.'''
        return self._dialect

    @dialect.setter
    def dialect(self, value):
        self._dialect = Dialect()
        if value:
            for attribute in dir(self._dialect):
                if '__' not in attribute:
                    setattr(self._dialect, attribute, getattr(value, attribute))

    def _row(self, row):
        dialect = self.dialect
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

    def writerow(self, row):
        '''Write a single row out to :meth:`file`, respecting any delimiters and
        header separators necessary.

        :param row: An iterable representing the row to write
        '''
        dialect = self.dialect
        if self.__wroteheader:
            if dialect.header_delimiter and dialect.corner_border:
                self._file.write(self._rowdelim(dialect.header_delimiter))
                self._file.write(dialect.lineterminator)
        elif self.__wroterow:
            if dialect.row_delimiter and dialect.corner_border:
                self._file.write(self._rowdelim(dialect.row_delimiter))
                self._file.write(dialect.lineterminator)

        self._file.write(self._row(row))
        self._file.write(dialect.lineterminator)

        self.__wroteheader = False
        self.__wroterow = True

    def writerows(self, rows):
        '''Write a multiple rows out to :meth:`file`, respecting any delimiters
        and header separators necessary.

        :param rows: An iterable of iterables representing the rows to write
        '''
        for row in rows:
            self.writerow(row)

    def writeheader(self, row):
        '''Write the header out to :meth:`file`.

        :param row: An iterable representing the row to write as a header
        '''
        self.writerow(row)
        self.__wroteheader = True

    def writetop(self):
        '''Write the top of the table out to :meth:`file`.'''
        dialect = self.dialect
        self._file.write(self._rowdelim(dialect.top_border))
        self._file.write(dialect.lineterminator)

    def writebottom(self):
        '''Write the bottom of the table out to :meth:`file`.'''
        dialect = self.dialect
        self._file.write(self._rowdelim(dialect.bottom_border))
        self._file.write(dialect.lineterminator)

class DictWriter(object):
    """Fixed-table document writer, writing tables with predefined column-sizes
    and names through dictionary rows passed in.

    The :class:`texttables.Dialect` class is used to configure how this writes
    tables.  This is a simple convenience frontend to
    :class:`texttables.fixed.writer`.
    This works as a context manager, in which case :meth:`writetop` and
    :meth:`writebottom` will be called automatically.
    """

    def __init__(self, file, fieldnames, widths, dialect=None, **fmtparams):
        """
        All the passed in construction parameters are passed to the
        :class:`texttables.fixed.writer` constructor literally.  All properties
        and most methods also align directly as well.
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

    @dialect.setter
    def dialect(self, value):
        self._writer.dialect = value

    @property
    def fieldnames(self):
        return self._fieldnames

    @fieldnames.setter
    def fieldnames(self, value):
        self._fieldnames = value

    def writeheader(self):
        '''Write the header based on :meth:`fieldnames`.'''
        self._writer.writeheader(self._fieldnames)

    def writerow(self, row):
        '''Write a single row out to :meth:`file`, respecting any delimiters and
        header separators necessary.

        :param row: A dictionary representing the row to write
        '''
        self._writer.writerow(row[field] for field in self._fieldnames)

    def writerows(self, rows):
        '''Write multiple rows out to :meth:`file`, respecting any delimiters and
        header separators necessary.

        :param row: An iterable of dictionaries representing the rows to write
        '''
        for row in rows:
            self.writerow(row)

    def writetop(self):
        self._writer.writetop()

    def writebottom(self):
        self._writer.writebottom()
