#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © 2016 Taylor C. Richberger <taywee@gmx.com>
# This code is released under the license described in the LICENSE file

import unittest
from six import StringIO

from texttables.fixed import writer

class WriterTest(unittest.TestCase):
    def test_basic_table(self):
        output = StringIO()

        data = (
            'header 1   header 2   header 3  \n'
            'data 1     data 2     data 3    \n'
            'data 4     data 5     data 6    \n'
            )
        with writer(output, [10, 10, 10]) as w:
            w.writeheader(('header 1', 'header 2', 'header 3'))
            w.writerow(('data 1', 'data 2', 'data 3'))
            w.writerow(('data 4', 'data 5', 'data 6'))

        self.assertEqual(data, output.getvalue())

if __name__ == '__main__':
    unittest.main()
