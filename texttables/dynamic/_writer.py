#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © 2017 Taylor C. Richberger <taywee@gmx.com>
# This code is released under the license described in the LICENSE file

from __future__ import division, absolute_import, print_function, unicode_literals
from six.moves import zip

from texttables.fixed import writer as fixedwriter

class writer(object):
    """Dynamic-table document writer, writing tables with computed column-sizes.
    The :class:`texttables.Dialect` class is used to configure how this writes
    tables.  This works as a context manager, in which case :meth:`finish` will
    be called automatically.
    This class does not actually write anything out until :meth:`finish` is
    called (or the context manager is exited) because it needs the information
    from all rows before it knows how wide to make all the columns."""

    def __init__(self, file, alignments=None, dialect=None, **fmtparams):
        """
        :param file: A writable file object with a ``write`` method
        :param alignments: An iterable of alignments.  Each alignment may be <,
            >, =, or ^, for alignment through the Python format specification.
        :param dialect: A dialect class or object used to define aspects of the
            table.  The stored dialect is always an instance of
            :class:`texttables.Dialect`, not necessarily the passed-in object.
            All the attributes of Dialect are grabbed from this object using
            getattr.
        :param fmtparams: parameters to override the parameters in
            :obj:`dialect`.
        """
        self._file = file
        self._alignments = alignments
        self._dialect = dialect
        self._fmtparams = fmtparams
        self._header = None
        self._rows = list()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.finish()

    @property
    def file(self):
        '''The file object that was passed in to the constructor.  It is not
        safe to change this object until you are finished using the class'''
        return self._file

    @property
    def dialect(self):
        '''The passed-in dialect.  This does not behave like the fixed dialects,
        because it does not actually construct a :class:`texttables.Dialect`
        until :meth:`finish` is called.'''
        return self._dialect

    @dialect.setter
    def dialect(self, value):
        self._dialect = value

    @property
    def rows(self):
        '''Get or set the total rows.  This will override all rows passed in
        with :meth:`writerow` and :meth:`writerows`'''
        return self._rows

    @rows.setter
    def rows(self, value):
        self._rows = value

    def writeheader(self, header):
        '''Set the header to be written out'''
        self._header = header

    def writerow(self, row):
        '''Add a row to the row set to be written out.  This does not write
        anything, and is only named as such for uniformity
        
        :param row: an iterable representing a row to write
        '''
        self._rows.append(row)

    def writerows(self, rows):
        '''Add rows to the row set to be written out.  This does not write
        anything, and is only named as such for uniformity

        :param rows: An iterable of iterables representing the rows to write
        '''
        self._rows.extend(rows)

    def finish(self):
        '''Write the top, the bottom, the header (if present), and all rows out
        with proper delimitation to :meth:`file`, respecting the dialect'''
        # Initiate all widths to 0
        widths = [0 for i in self._rows[0]]

        def checkwidths(row):
            for i in range(len(row)):
                size = len(row[i])
                if size > widths[i]:
                    widths[i] = size

        # Iterate all rows to find which is the largest cell for each column
        checkwidths(self._header)
        for row in self._rows:
            checkwidths(row)


        if self._alignments is not None:
            widths = ['{}{}'.format(alignment, width) for alignment, width in zip(self._alignments, widths)]

        with fixedwriter(self._file, widths, self._dialect, **self._fmtparams) as w:
            header = self._header
            if header is not None:
                w.writeheader(header)

            for row in self._rows:
                w.writerow(row) 

class DictWriter(object):
    """Dynamic-table document writer, writing tables with predefined column-sizes
    and names through dictionary rows passed in.

    The :class:`texttables.Dialect` class is used to configure how this writes
    tables.  This is a simple convenience frontend to
    :class:`texttables.dynamic.writer`.
    This works as a context manager, in which case :meth:`finish` will be called
    automatically.
    """

    def __init__(self, file, fieldnames, alignments=None, dialect=None, **fmtparams):
        """
        All the passed in construction parameters are passed to the
        :class:`texttables.dynamic.writer` constructor literally.  All
        properties and most methods also align directly as well.
        """

        self._writer = writer(file, alignments, dialect, **fmtparams)
        self._fieldnames = fieldnames

    def __enter__(self):
        self._writer.__enter__()
        return self

    def __exit__(self, type, value, traceback):
        self._writer.__exit__(type, value, traceback)

    @property
    def file(self):
        return self._writer.file

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
        '''Set the header based on :meth:`fieldnames`.'''
        self._writer.writeheader(self._fieldnames)

    def writerow(self, row):
        '''Write a row based on :meth:`fieldnames`.

        :param row: A dictionary representing a row.'''
        self._writer.writerow(tuple(row[field] for field in self._fieldnames))

    def writerows(self, rows):
        '''Write rows based on :meth:`fieldnames`.

        :param row: An iterable of dictionaries representing rows.'''
        for row in rows:
            self.writerow(row)
