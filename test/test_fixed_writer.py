#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © 2016 Taylor C. Richberger <taywee@gmx.com>
# This code is released under the license described in the LICENSE file

import unittest
from six import StringIO

from texttables.fixed import writer
from texttables import Dialect

class FixedWriterTest(unittest.TestCase):
    def run_asserts(self, writer, data, output):
        with writer as w:
            w.writeheader(('header 1', 'header 2', 'header 3'))
            w.writerow(('data 1', 'data 2', 'data 3'))
            w.writerow(('data 4', 'data 5', 'data 6'))

        self.assertEqual(data, output.getvalue())

    def test_basic_table(self):
        output = StringIO()
        data = (
            'header 1   header 2   header 3  \n'
            'data 1     data 2     data 3    \n'
            'data 4     data 5     data 6    \n'
            )
        self.run_asserts(writer(output, [10, 10, 10]), data, output)

    def test_basic_table_header_delim(self):
        class dialect(Dialect):
            header_delimiter = '='
            corner_border = ' '
        output = StringIO()
        data = (
            'header 1   header 2   header 3  \n'
            '========== ========== ==========\n'
            'data 1     data 2     data 3    \n'
            'data 4     data 5     data 6    \n'
            )
        self.run_asserts(writer(output, [10, 10, 10], dialect=dialect), data, output)


    def test_basic_table_header_row_delim(self):
        class dialect(Dialect):
            header_delimiter = '='
            row_delimiter = '-'
            corner_border = ' '

        output = StringIO()
        data = (
            'header 1   header 2   header 3  \n'
            '========== ========== ==========\n'
            'data 1     data 2     data 3    \n'
            '---------- ---------- ----------\n'
            'data 4     data 5     data 6    \n'
            )
        self.run_asserts(writer(output, [10, 10, 10], dialect=dialect), data, output)

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
        self.run_asserts(writer(output, [10, 10, 10], dialect=dialect), data, output)

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
        self.run_asserts(writer(output, [10, 10, 10], dialect=dialect), data, output)

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
        self.run_asserts(writer(output, [10, '>10', '^10'], dialect=dialect), data, output)

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

        # we don't use "run_asserts" here because we want to test writerows
        with writer(output, [10, '>10', '^10'], dialect=dialect) as w:
            w.writeheader(('header 1', 'header 2', 'header 3'))
            w.writerows([
                ('data 1', 'data 2', 'data 3'),
                ('data 4', 'data 5', 'data 6')])

        data = (
            '+##########+##########+##########+\n'
            '|header 1  |  header 2| header 3 |\n'
            '+==========+==========+==========+\n'
            '|data 1    |    data 2|  data 3  |\n'
            '+----------+----------+----------+\n'
            '|data 4    |    data 5|  data 6  |\n'
            '+__________+__________+__________+\n'
            )
        self.assertEqual(data, output.getvalue())

if __name__ == '__main__':
    unittest.main()
