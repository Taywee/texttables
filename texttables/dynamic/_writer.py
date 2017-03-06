#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © 2017 Taylor C. Richberger <taywee@gmx.com>
# This code is released under the license described in the LICENSE file

from __future__ import division, absolute_import, print_function, unicode_literals
from six.moves import zip

from texttables.fixed import writer as fixedwriter

class writer(object):
    """Dynamic-table document writer, writing tables with computed column-sizes"""

    def __init__(self, file, alignments=None, dialect=None, **fmtparams):
        """
        :file: A writable file object with a ``write`` method
        :alignments: List of string alignments, as the prefixes passed to
         texttables.fixed.writer's widths argument
        :dialect: A dialect class used to define aspects of the table.
        :fmtparams: parameters to override the parameters in dialect.
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
        return self._file

    @property
    def dialect(self):
        return self._dialect

    @property
    def rows(self):
        return self._rows

    @rows.setter
    def rows(self, value):
        self._rows = value

    def writeheader(self, header):
        self._header = header

    def writerow(self, row):
        self._rows.append(row)

    def writerows(self, rows):
        self._rows.extend(rows)

    def finish(self):
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
    and names"""

    def __init__(self, file, fieldnames, alignments=None, dialect=None, **fmtparams):
        """
        :file: A writable file object with a ``write`` method
        :fieldnames: A sequence of field names
        :dialect: A dialect class used to define aspects of the table.
         Each width may be prefixed with <, >, =, or ^, for alignment through
         the Python format specification.
        :fmtparams: parameters to override the parameters in dialect.
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
        self._writer.writeheader(self._fieldnames)

    def writerow(self, row):
        self._writer.writerow(tuple(row[field] for field in self._fieldnames))

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
