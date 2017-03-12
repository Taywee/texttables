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

########
Examples
########

***********************
texttables.fixed.writer
***********************

::

    >>> from texttables import Dialect
    >>> from texttables.fixed import writer
    >>> from sys import stdout
    >>> 
    >>> with writer(stdout, [10, 10, 10]) as w:
    ...     w.writeheader(('header 1', 'header 2', 'header 3'))
    ...     w.writerow(('data 1', 'data 2', 'data 3'))
    ...     w.writerow(('data 4', 'data 5', 'data 6'))
    ... 
    header 1   header 2   header 3  
    data 1     data 2     data 3    
    data 4     data 5     data 6    

******************
texttables.Dialect
******************

::

    >>> from texttables import Dialect
    >>> from texttables.fixed import writer
    >>> from sys import stdout
    >>> class dialect(Dialect):
    ...     header_delimiter = '='
    ...     row_delimiter = '-'
    ...     top_border = '#'
    ...     bottom_border = '_'
    ...     left_border = '|'
    ...     cell_delimiter = '|'
    ...     right_border = '|'
    ...     corner_border = '+'
    ...
    >>> with writer(stdout, [10, 10, 10], dialect=dialect) as w:
    ...     w.writeheader(('header 1', 'header 2', 'header 3'))
    ...     w.writerow(('data 1', 'data 2', 'data 3'))
    ...     w.writerow(('data 4', 'data 5', 'data 6'))
    ...
    +##########+##########+##########+
    |header 1  |header 2  |header 3  |
    +==========+==========+==========+
    |data 1    |data 2    |data 3    |
    +----------+----------+----------+
    |data 4    |data 5    |data 6    |
    +__________+__________+__________+

***************************
texttables.fixed.DictWriter
***************************

::

    >>> from texttables import Dialect
    >>> from texttables.fixed import DictWriter
    >>> from sys import stdout
    >>> class dialect(Dialect):
    ...     header_delimiter = '='
    ...     row_delimiter = '-'
    ...     top_border = '#'
    ...     bottom_border = '_'
    ...     left_border = '|'
    ...     cell_delimiter = '|'
    ...     right_border = '|'
    ...     corner_border = '+'
    ...
    >>> with DictWriter(stdout, ['foo', 'bar', 'baz'], [10, '>10', '^10'], dialect=dialect) as w:
    ...     w.writeheader()
    ...     w.writerow({'foo': 'data 1', 'bar': 'data 2', 'baz': 'data 3'})
    ...     w.writerow({'foo': 'data 4', 'bar': 'data 5', 'baz': 'data 6'})
    ...
    +##########+##########+##########+
    |foo       |       bar|   baz    |
    +==========+==========+==========+
    |data 1    |    data 2|  data 3  |
    +----------+----------+----------+
    |data 4    |    data 5|  data 6  |
    +__________+__________+__________+

***********************
texttables.fixed.reader
***********************

::

    >>> from texttables import Dialect
    >>> from texttables.fixed import reader
    >>> from sys import stdout
    >>>
    >>> class dialect(Dialect):
    ...     header_delimiter = '='
    ...     row_delimiter = '-'
    ...     top_border = '#'
    ...     bottom_border = '_'
    ...     left_border = '|'
    ...     cell_delimiter = '|'
    ...     right_border = '|'
    ...     corner_border = '+'
    ...
    >>> data = (
    ...     '+##########+##########+##########+\n'
    ...     '|header 1  |  header 2| header 3 |\n'
    ...     '+==========+==========+==========+\n'
    ...     '|data 1    |    data 2|  data 3  |\n'
    ...     '+----------+----------+----------+\n'
    ...     '|data 4    |    data 5|  data 6  |\n'
    ...     '+__________+__________+__________+\n'
    ...     )
    >>> r = reader(data.splitlines(), [10, 10, 10], dialect=dialect)
    >>> rows = [row for row in r]
    >>> r.fieldnames
    ('header 1', 'header 2', 'header 3')
    >>> rows
    [('data 1', 'data 2', 'data 3'), ('data 4', 'data 5', 'data 6')]

***************************
texttables.fixed.DictReader
***************************

::

    >>> from texttables import Dialect
    >>> from texttables.fixed import DictReader
    >>> from sys import stdout
    >>>
    >>> class dialect(Dialect):
    ...     header_delimiter = '='
    ...     row_delimiter = '-'
    ...     top_border = '#'
    ...     bottom_border = '_'
    ...     left_border = '|'
    ...     cell_delimiter = '|'
    ...     right_border = '|'
    ...     corner_border = '+'
    ...
    >>> data = (
    ...     '+##########+##########+##########+\n'
    ...     '|header 1  |  header 2| header 3 |\n'
    ...     '+==========+==========+==========+\n'
    ...     '|data 1    |    data 2|  data 3  |\n'
    ...     '+----------+----------+----------+\n'
    ...     '|data 4    |    data 5|  data 6  |\n'
    ...     '+__________+__________+__________+\n'
    ...     )
    >>> r = DictReader(data.splitlines(), [10, 10, 10], dialect=dialect)
    >>> rows = [row for row in r]
    >>> rows
    [{'header 3': 'data 3', 'header 2': 'data 2', 'header 1': 'data 1'}, {'header 3': 'data 6', 'header 2': 'data 5', 'header 1': '
    data 4'}]

**************************
texttables.ValidationError
**************************

::

    >>> from texttables import Dialect
    >>> from texttables.fixed import DictReader
    >>> from sys import stdout
    >>>
    >>> class dialect(Dialect):
    ...     header_delimiter = '='
    ...     row_delimiter = '-'
    ...     top_border = '#'
    ...     bottom_border = '_'
    ...     left_border = '|'
    ...     cell_delimiter = '|'
    ...     right_border = '|'
    ...     corner_border = '+'
    ...
    >>> data = (
    ...     '|header 1  |  header 2| header 3 |\n'
    ...     '+==========+==========+==========+\n'
    ...     '|data 1    |    data 2|  data 3  |\n'
    ...     '+----------+----------+----------+\n'
    ...     '|data 4    |    data 5|  data 6  |\n'
    ...     '+__________+__________+__________+\n'
    ...     )
    >>> r = DictReader(data.splitlines(), [10, 10, 10], dialect=dialect)
    >>> rows = [row for row in r]
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "<stdin>", line 1, in <listcomp>
      File "/home/taylor/Projects/texttables/texttables/fixed/_reader.py", line 273, in __next__
        row = next(self._iter)
      File "/home/taylor/Projects/texttables/texttables/fixed/_reader.py", line 205, in __next__
        fieldnames = self.fieldnames
      File "/home/taylor/Projects/texttables/texttables/fixed/_reader.py", line 135, in fieldnames
        raise ValidationError('The first line of the table did not match what the top of the table should be')
    texttables.errors.ValidationError: The first line of the table did not match what the top of the table should be

*************************
texttables.dynamic.writer
*************************

::

    >>> from texttables import Dialect
    >>> from texttables.dynamic import writer
    >>> from sys import stdout
    >>>
    >>> class dialect(Dialect):
    ...     header_delimiter = '='
    ...     row_delimiter = '-'
    ...     top_border = '#'
    ...     bottom_border = '_'
    ...     left_border = '|'
    ...     cell_delimiter = '|'
    ...     right_border = '|'
    ...     corner_border = '+'
    ...
    >>> with writer(stdout, ['', '>', '^'], dialect=dialect) as w:
    ...     w.writeheader(('header 1', 'header 2', 'header 3'))
    ...     w.writerows([
    ...         ('data 1', 'data 2', 'data 3'),
    ...         ('data 4', 'data 5', 'data 6')])
    ...
    +########+########+########+
    |header 1|header 2|header 3|
    +========+========+========+
    |data 1  |  data 2| data 3 |
    +--------+--------+--------+
    |data 4  |  data 5| data 6 |
    +________+________+________+

*****************************
texttables.dynamic.DictWriter
*****************************

::

    >>> from texttables import Dialect
    >>> from texttables.dynamic import DictWriter
    >>> from sys import stdout
    >>>
    >>> class dialect(Dialect):
    ...     header_delimiter = '='
    ...     corner_border = ' '
    ...
    >>> with DictWriter(stdout, ['foo', 'bar', 'baz'], dialect=dialect) as w:
    ...     w.writeheader()
    ...     w.writerows([
    ...         {'foo': 'data 1', 'bar': 'data 2', 'baz': 'data 3'},
    ...         {'foo': 'data 4', 'bar': 'data 5', 'baz': 'data 6'}])
    ...
    foo    bar    baz
    ====== ====== ======
    data 1 data 2 data 3
    data 4 data 5 data 6

##################
Indices and tables
##################

* :ref:`genindex`
* :ref:`search`

#######
License
#######

This module is released under the MIT license.
