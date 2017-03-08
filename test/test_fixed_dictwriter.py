#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © 2016 Taylor C. Richberger <taywee@gmx.com>
# This code is released under the license described in the LICENSE file

import unittest
from six import StringIO

from texttables.fixed import DictWriter
from texttables import Dialect

class FixedDictWriterTest(unittest.TestCase):
    def run_asserts(self, writer, data, output):
        with writer as w:
            w.writeheader()
            w.writerow({'foo': 'data 1', 'bar': 'data 2', 'baz': 'data 3'})
            w.writerow({'foo': 'data 4', 'bar': 'data 5', 'baz': 'data 6'})

        self.assertEqual(data, output.getvalue())

    def test_basic_table(self):
        output = StringIO()
        data = (
            'foo        bar        baz       \n'
            'data 1     data 2     data 3    \n'
            'data 4     data 5     data 6    \n'
            )
        self.run_asserts(DictWriter(output, ['foo', 'bar', 'baz'], [10, 10, 10]), data, output)

    def test_basic_table_header_delim(self):
        class dialect(Dialect):
            header_delimiter = '='
            corner_border = ' '
        output = StringIO()
        data = (
            'foo        bar        baz       \n'
            '========== ========== ==========\n'
            'data 1     data 2     data 3    \n'
            'data 4     data 5     data 6    \n'
            )
        self.run_asserts(DictWriter(output, ['foo', 'bar', 'baz'], [10, 10, 10], dialect=dialect), data, output)

    def test_basic_table_header_row_delim(self):
        class dialect(Dialect):
            header_delimiter = '='
            row_delimiter = '-'
            corner_border = ' '

        output = StringIO()
        data = (
            'foo        bar        baz       \n'
            '========== ========== ==========\n'
            'data 1     data 2     data 3    \n'
            '---------- ---------- ----------\n'
            'data 4     data 5     data 6    \n'
            )
        self.run_asserts(DictWriter(output, ['foo', 'bar', 'baz'], [10, 10, 10], dialect=dialect), data, output)

    def test_basic_table_row_delim(self):
        class dialect(Dialect):
            header_delimiter = None
            row_delimiter = '-'
            corner_border = ' '

        output = StringIO()
        data = (
            'foo        bar        baz       \n'
            'data 1     data 2     data 3    \n'
            '---------- ---------- ----------\n'
            'data 4     data 5     data 6    \n'
            )
        self.run_asserts(DictWriter(output, ['foo', 'bar', 'baz'], [10, 10, 10], dialect=dialect), data, output)

    def test_full_borders(self):
        class dialect(Dialect):
            header_delimiter = '='
            row_delimiter = '-'
            top_border = '#'
            bottom_border = '_'
            left_border = '|'
            cell_delimiter = '|'
            right_border = '|'
            corner_border = '+'
        output = StringIO()

        data = (
            '+##########+##########+##########+\n'
            '|foo       |bar       |baz       |\n'
            '+==========+==========+==========+\n'
            '|data 1    |data 2    |data 3    |\n'
            '+----------+----------+----------+\n'
            '|data 4    |data 5    |data 6    |\n'
            '+__________+__________+__________+\n'
            )
        self.run_asserts(DictWriter(output, ['foo', 'bar', 'baz'], [10, 10, 10], dialect=dialect), data, output)

    def test_alignment(self):
        class dialect(Dialect):
            header_delimiter = '='
            row_delimiter = '-'
            top_border = '#'
            bottom_border = '_'
            left_border = '|'
            cell_delimiter = '|'
            right_border = '|'
            corner_border = '+'
        output = StringIO()

        data = (
            '+##########+##########+##########+\n'
            '|foo       |       bar|   baz    |\n'
            '+==========+==========+==========+\n'
            '|data 1    |    data 2|  data 3  |\n'
            '+----------+----------+----------+\n'
            '|data 4    |    data 5|  data 6  |\n'
            '+__________+__________+__________+\n'
            )
        self.run_asserts(DictWriter(output, ['foo', 'bar', 'baz'], [10, '>10', '^10'], dialect=dialect), data, output)

    def test_writerows(self):
        class dialect(Dialect):
            header_delimiter = '='
            row_delimiter = '-'
            top_border = '#'
            bottom_border = '_'
            left_border = '|'
            cell_delimiter = '|'
            right_border = '|'
            corner_border = '+'
        output = StringIO()

        with DictWriter(output, ['foo', 'bar', 'baz'], [10, '>10', '^10'], dialect=dialect) as w:
            w.writeheader()
            w.writerows([
                {'foo': 'data 1', 'bar': 'data 2', 'baz': 'data 3'},
                {'foo': 'data 4', 'bar': 'data 5', 'baz': 'data 6'}])

        data = (
            '+##########+##########+##########+\n'
            '|foo       |       bar|   baz    |\n'
            '+==========+==========+==========+\n'
            '|data 1    |    data 2|  data 3  |\n'
            '+----------+----------+----------+\n'
            '|data 4    |    data 5|  data 6  |\n'
            '+__________+__________+__________+\n'
            )
        self.assertEqual(data, output.getvalue())

if __name__ == '__main__':
    unittest.main()
