.. texttables documentation master file, created by
   sphinx-quickstart on Sun Mar 12 09:59:38 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

########################
texttables python module
########################

This is a simple python module for reading and writing ASCII text tables.  It
attempts to have an interface as similar to Python's official :mod:`csv` module
as possible.  It supports fixed-size tables (where column sizes are pre-decided)
for reading and writing (including with a dictionary).  It supports
dynamic-sized tables (where each column's width is deduced to be the largest
element in that column) for writing only, including dict writing.

There are less obvious uses to this module, such as being able to use a sort of
TSV that is width-delimited rather than character-delimited.

There is a small `unit test suite
<https://github.com/Taywee/texttables/tree/master/test>`__ that attempts to
catch obvious issues.  Pull requests to any of this module are welcome, as long
as the license remains the same.

The sources are available in the `GitHub Repository
<https://github.com/Taywee/texttables>`__.

*************
Fixed Readers
*************

texttables.fixed.reader
=======================

.. autoclass:: texttables.fixed.reader
    :members:

texttables.fixed.DictReader
===========================

.. autoclass:: texttables.fixed.DictReader
    :members:

*************
Fixed Writers
*************

texttables.fixed.writer
=======================

.. autoclass:: texttables.fixed.writer
    :members:

texttables.fixed.DictWriter
===========================

.. autoclass:: texttables.fixed.DictWriter
    :members:

***************
Dynamic Writers
***************

texttables.dynamic.writer
=========================

.. autoclass:: texttables.dynamic.writer
    :members:

texttables.dynamic.DictWriter
=============================

.. autoclass:: texttables.dynamic.DictWriter
    :members:

******************
texttables.Dialect
******************

.. autoclass:: texttables.Dialect
    :members:

**************************
texttables.ValidationError
**************************

.. autoclass:: texttables.ValidationError
    :members:

##################
Indices and tables
##################

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

#######
License
#######

This module is released under the MIT license.
