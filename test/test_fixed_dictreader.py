#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © 2016 Taylor C. Richberger <taywee@gmx.com>
# This code is released under the license described in the LICENSE file

import unittest
from six import StringIO

from texttables.fixed import DictReader as reader
from texttables import Dialect
from texttables import ValidationError

class FixedDictReaderTest(unittest.TestCase):
    def run_unstripped_asserts(self, reader):
        self.assertEqual(reader.fieldnames, ('header 1  ', 'header 2  ', 'header 3  '))
        rows = list()
        rows = [row for row in reader]
        self.assertEqual(rows, [
            {'header 1  ': 'data 1    ', 'header 2  ': 'data 2    ', 'header 3  ': 'data 3    '},
            {'header 1  ': 'data 4    ', 'header 2  ': 'data 5    ', 'header 3  ': 'data 6    '},
            ])

    def run_asserts(self, reader):
        self.assertEqual(reader.fieldnames, ('header 1', 'header 2', 'header 3'))
        rows = list()
        rows = [row for row in reader]
        self.assertEqual(rows, [
            {'header 1': 'data 1', 'header 2': 'data 2', 'header 3': 'data 3'},
            {'header 1': 'data 4', 'header 2': 'data 5', 'header 3': 'data 6'},
            ])

    def test_basic_table(self):
        data = (
            'header 1   header 2   header 3  \n'
            'data 1     data 2     data 3    \n'
            'data 4     data 5     data 6    \n'
            )
        self.run_asserts(reader(data.splitlines(), [10, 10, 10]))

    def test_basic_table_header_delim(self):
        class dialect(Dialect):
            header_delimiter = '='
            corner_border = ' '
        data = (
            'header 1   header 2   header 3  \n'
            '========== ========== ==========\n'
            'data 1     data 2     data 3    \n'
            'data 4     data 5     data 6    \n'
            )
        self.run_asserts(reader(data.splitlines(), [10, 10, 10], dialect=dialect))

    def test_basic_table_header_top_bottom_delim(self):
        class dialect(Dialect):
            header_delimiter = '='
            top_border = '='
            bottom_border = '='
            corner_border = ' '

        output = StringIO()
        data = (
            '========== ========== ==========\n'
            'header 1   header 2   header 3  \n'
            '========== ========== ==========\n'
            'data 1     data 2     data 3    \n'
            'data 4     data 5     data 6    \n'
            '========== ========== ==========\n'
            )
        self.run_asserts(reader(data.splitlines(), [10, 10, 10], dialect=dialect))

    def test_basic_table_header_row_delim(self):
        class dialect(Dialect):
            header_delimiter = '='
            row_delimiter = '-'
            corner_border = ' '
            strip = False

        output = StringIO()
        data = (
            'header 1   header 2   header 3  \n'
            '========== ========== ==========\n'
            'data 1     data 2     data 3    \n'
            '---------- ---------- ----------\n'
            'data 4     data 5     data 6    \n'
            )
        self.run_unstripped_asserts(reader(data.splitlines(), [10, 10, 10], dialect=dialect))

    def test_basic_table_row_delim(self):
        class dialect(Dialect):
            header_delimiter = None
            row_delimiter = '-'
            corner_border = ' '

        output = StringIO()
        data = (
            'header 1   header 2   header 3  \n'
            'data 1     data 2     data 3    \n'
            '---------- ---------- ----------\n'
            'data 4     data 5     data 6    \n'
            )
        self.run_asserts(reader(data.splitlines(), [10, 10, 10], dialect=dialect))

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
            '|header 1  |header 2  |header 3  |\n'
            '+==========+==========+==========+\n'
            '|data 1    |data 2    |data 3    |\n'
            '+----------+----------+----------+\n'
            '|data 4    |data 5    |data 6    |\n'
            '+__________+__________+__________+\n'
            )
        self.run_asserts(reader(data.splitlines(), [10, 10, 10], dialect=dialect))

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
            '|header 1  |  header 2| header 3 |\n'
            '+==========+==========+==========+\n'
            '|data 1    |    data 2|  data 3  |\n'
            '+----------+----------+----------+\n'
            '|data 4    |    data 5|  data 6  |\n'
            '+__________+__________+__________+\n'
            )
        self.run_asserts(reader(data.splitlines(), [10, 10, 10], dialect=dialect))

    def test_strict_top(self):
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
            '|header 1  |  header 2| header 3 |\n'
            '+==========+==========+==========+\n'
            '|data 1    |    data 2|  data 3  |\n'
            '+----------+----------+----------+\n'
            '|data 4    |    data 5|  data 6  |\n'
            '+__________+__________+__________+\n'
            )
        with self.assertRaises(ValidationError):
            rows = [row for row in reader(data.splitlines(), [10, 10, 10], dialect=dialect)]

    def test_strict_bottom(self):
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
            '|header 1  |  header 2| header 3 |\n'
            '+==========+==========+==========+\n'
            '|data 1    |    data 2|  data 3  |\n'
            '+----------+----------+----------+\n'
            '|data 4    |    data 5|  data 6  |\n'
            )
        with self.assertRaises(ValidationError):
            rows = [row for row in reader(data.splitlines(), [10, 10, 10], dialect=dialect)]

    def test_strict_left(self):
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
            '##########+##########+##########+\n'
            'header 1  |  header 2| header 3 |\n'
            '==========+==========+==========+\n'
            'data 1    |    data 2|  data 3  |\n'
            '----------+----------+----------+\n'
            'data 4    |    data 5|  data 6  |\n'
            '__________+__________+__________+\n'
            )
        with self.assertRaises(ValidationError):
            rows = [row for row in reader(data.splitlines(), [10, 10, 10], dialect=dialect)]

    def test_strict_right(self):
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
            '+##########+##########+##########\n'
            '|header 1  |  header 2| header 3 \n'
            '+==========+==========+==========\n'
            '|data 1    |    data 2|  data 3  \n'
            '+----------+----------+----------\n'
            '|data 4    |    data 5|  data 6  \n'
            '+__________+__________+__________\n'
            )
        with self.assertRaises(ValidationError):
            rows = [row for row in reader(data.splitlines(), [10, 10, 10], dialect=dialect)]

    def test_strict_cell(self):
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
            '|header 1  |  header 2| header 3 |\n'
            '+==========+==========+==========+\n'
            '|data 1         data 2|  data 3  |\n'
            '+----------+----------+----------+\n'
            '|data 4    |    data 5|  data 6  |\n'
            '+__________+__________+__________+\n'
            )
        with self.assertRaises(ValidationError):
            rows = [row for row in reader(data.splitlines(), [10, 10, 10], dialect=dialect)]

    def test_no_strict_cell(self):
        class dialect(Dialect):
            header_delimiter = '='
            row_delimiter = '-'
            top_border = '#'
            bottom_border = '_'
            left_border = '|'
            cell_delimiter = '|'
            right_border = '|'
            corner_border = '+'
            strict = False
        output = StringIO()

        data = (
            '+##########+##########+##########+\n'
            '|header 1  |  header 2| header 3 |\n'
            '+==========+==========+==========+\n'
            '|data 1         data 2|  data 3  |\n'
            '+----------+----------+----------+\n'
            '|data 4    |    data 5|  data 6  |\n'
            '+__________+__________+__________+\n'
            )
        rows = [row for row in reader(data.splitlines(), [10, 10, 10], dialect=dialect)]

    def test_strict_header(self):
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
            '|header 1  |  header 2| header 3 |\n'
            '|data 1    |    data 2|  data 3  |\n'
            '+----------+----------+----------+\n'
            '|data 4    |    data 5|  data 6  |\n'
            '+__________+__________+__________+\n'
            )
        with self.assertRaises(ValidationError):
            rows = [row for row in reader(data.splitlines(), [10, 10, 10], dialect=dialect)]

    def test_strict_row(self):
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
            '|header 1  |  header 2| header 3 |\n'
            '+==========+==========+==========+\n'
            '|data 1    |    data 2|  data 3  |\n'
            '|data 4    |    data 5|  data 6  |\n'
            '+__________+__________+__________+\n'
            )
        with self.assertRaises(ValidationError):
            rows = [row for row in reader(data.splitlines(), [10, 10, 10], dialect=dialect)]

    def test_samebottom(self):
        class dialect(Dialect):
            header_delimiter = '='
            row_delimiter = '-'
            top_border = '#'
            bottom_border = '-'
            left_border = '|'
            cell_delimiter = '|'
            right_border = '|'
            corner_border = '+'
        output = StringIO()

        data = (
            '+##########+##########+##########+\n'
            '|header 1  |  header 2| header 3 |\n'
            '+==========+==========+==========+\n'
            '|data 1    |    data 2|  data 3  |\n'
            '+----------+----------+----------+\n'
            '|data 4    |    data 5|  data 6  |\n'
            '+----------+----------+----------+\n'
            )
        self.run_asserts(reader(data.splitlines(), [10, 10, 10], dialect=dialect))

    def test_nofieldnames(self):
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
            '|data 1    |    data 2|  data 3  |\n'
            '+----------+----------+----------+\n'
            '|data 4    |    data 5|  data 6  |\n'
            '+__________+__________+__________+\n'
            )
        self.run_asserts(reader(data.splitlines(), [10, 10, 10], fieldnames=('header 1', 'header 2', 'header 3'), dialect=dialect))

if __name__ == '__main__':
    unittest.main()
