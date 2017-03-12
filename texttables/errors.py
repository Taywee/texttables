#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © 2017 Taylor C. Richberger <taywee@gmx.com>
# This code is released under the license described in the LICENSE file

class ValidationError(Exception):
    '''This is raised if :attr:`texttables.Dialect.strict` is True and an
    invalid table is read.'''
