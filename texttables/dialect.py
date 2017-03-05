#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © 2017 Taylor C. Richberger <taywee@gmx.com>
# This code is released under the license described in the LICENSE file

from __future__ import division, absolute_import, print_function, unicode_literals
import six

class Dialect(object):
    """Class that is mostly subclassed for use in tables.  Some attributes might
    only be used for either a dynamic or fixed table, but not both.
    horizontal_border, corner_border, and header_border must either all be set
    or all be None."""

    header_delimiter = '='
    row_delimiter = None
    cell_delimiter = ' '
    left_border = None
    right_border = None
    top_border = None
    bottom_border = None
    corner_border = None
    lineterminator = '\n'
    strict = False

_DIALECTFIELDS = {
    'header_delimiter',
    'row_delimiter',
    'cell_delimiter',
    'left_border',
    'right_border',
    'top_border',
    'bottom_border',
    'corner_border',
    'lineterminator',
    'strict',
    }
