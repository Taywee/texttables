#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © 2016 Absolute Performance Inc <csteam@absolute-performance.com>.
# All rights reserved.
# This is proprietary software.
# No warranty, explicit or implicit, provided.

from __future__ import division, absolute_import, print_function, unicode_literals

__author__ = 'Taylor C. Richberger <tcr@absolute-performance.com>'
__description__ = 'A Python module for parsing and writing text-based tables'
__email__ = 'tcr@absolute-performance.com'
__license__ = 'MIT'
__modulename__ = 'texttables'
__version__ = '1.0.0'
__website__ = 'https://github.com/Taywee/texttables'

__all__ = ['fixed', 'dynamic', 'ValidationError', 'Dialect']

from .errors import ValidationError
from . import fixed
from . import dynamic
from .dialect import Dialect
