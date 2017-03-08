#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © 2017 Taylor C. Richberger <taywee@gmx.com>
# This code is released under the license described in the LICENSE file

from __future__ import division, absolute_import, print_function, unicode_literals
import six

class Dialect(object):
    """Class that is mostly subclassed for use in tables.  Some attributes might
    only be used for either a dynamic or fixed table, but not both.  Likewise,
    some attributes might only be used for a reader or writer.  This can be
    instantiated and have the attributes changed instead of subclassing, for
    one-offs, but subclassing is usually clearer."""

    #: Delimiter character separating header from rows.  None to disable
    header_delimiter = None

    #: Delimiter character separating rows from one another.  None to disable
    row_delimiter = None

    #: Delimiter character separating cells from one another.  Must exist.
    cell_delimiter = ' '

    #: Border character for non-corners on the left side of each row. None to
    #: disable
    left_border = None

    #: Border character for non-corners on the right side of each row. None to
    #: disable
    right_border = None

    #: Border character for non-corners on the top side of the top cells.  None
    #: to disable
    top_border = None

    #: Border character for non-corners on the bottom side of the bottom cells.
    #: None to disable
    bottom_border = None

    #: Border character for corners on each border and on the row and header
    #: delimiters.  Required when the borders or delimiters are specified.
    corner_border = '+'

    #: Line terminator.  Used only for writing tables, and ignored on reading
    lineterminator = '\n'

    #: Whether to raise an exception on read errors, such as borders appearing
    #: in the wrong order or missing borders.
    strict = True

    #: Whether to strip fields on reads.  This is usually desired, especially
    #: for DictReader types.
    strip = True
