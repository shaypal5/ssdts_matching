ssdts_matching
##############
|PyPI-Status| |PyPI-Versions| |Build-Status| |Codecov| |LICENCE|

Fast optimal matching of items for source-sharing derivative time series.

.. code-block:: python

  from ssdts_matching import dynamic_timestamp_match
  dynamic_timestamp_match(timestamp1, timestamps2, delta=20)

.. contents::

.. section-numbering::

Installation
============

Install ``ssdts_matching`` with:

.. code-block:: bash

  pip install ssdts_matching


Features
========

* Pure Python.
* Compatible with Python 3.5+.
* Dependencies:

  * numpy
  * `sortedcontainers <https://pypi.python.org/pypi/sortedcontainers>`_


Use
===

You can get a matching of two timestamp series with

.. code-block:: python

  from ssdts_matching import dynamic_timestamp_match
  dynamic_timestamp_match(timestamp1, timestamps2, delta=20)


Six different functions, in an increasing level of complexity, are procided:


popping_greedy_timestamp_match
------------------------------

Tries to match two timestamp series in a greedy fashion. Timestamps are popped from their lists as they are matched.

Runs in ``O(M*log(N))`` where ``M=len(timestamps1)`` and ``M=len(timestamps2)``. Not guarenteed to find an optimal matching error-wise, where the error is the sum of differences between matched pairs.


greedy_timestamp_match
----------------------

Tries to match two timestamp series in a greedy fashion.

Runs in ``O(M*log(N))`` where ``M=len(timestamps1)`` and ``M=len(timestamps2)``. If the resulting match is an injective function from the first series to the second one then the solution is optimal error-wise, where the error is the sum of differences between matched pairs. Otherwise, it is not.


dynamic_timestamp_match
-----------------------

Optimally matches two timestamp series using dynamic programming.

Runs in ``O(M*N)``, where ``M=len(timestamps1)`` and ``N=len(timestamps2)``. Guarentees an optimal solution error-wise, where the error is the sum of differences between matched pairs.


hybrid_timestamp_match
----------------------

Finds the optimal matching of two timestamps series using both a greedy algorithm and a dynamic one.

Runs in ``O(M*N)``, where ``M=len(timestamps1)`` and ``N=len(timestamps2)``, but has a better average running time than ``dynamic_timestamp_match`` if some inputs can be optimally solved with the greedy algorithm. Guarentees an optimal solution error-wise, where the error is the sum of differences between matched pairs.


vertical_aligned_timestamp_match
--------------------------------

Matches two timestamps series by partioning them by verticals (pairs of timestamps from both series with identical values) and matching each partition using the hybrid approach.

Runs in O(M*N), where ``M=len(timestamps1)`` and ``N=len(timestamps2)``. Does not guarentee an optimal solution error-wise, where the error is the sum of differences between matched pairs.


delta_partitioned_timestamp_match
---------------------------------

ttempts to match the two given series of timestamps by partioning the first series into ``2 * delta``-separated buckets, and applying the given matching function to each (any of the above functions can be used), combining the sub-solution into a matching.

If the provided matching function yields optimal matchings, than so is the matching provided by this function. The algorithm is not guarenteed to be symmetric; giving the same two series in the opposite order may yield a different matching.


Contributing
============

Package author and current maintainer is Shay Palachy (shay.palachy@gmail.com); You are more than welcome to approach him for help. Contributions are very welcomed.

Installing for development
--------------------------

Clone:

.. code-block:: bash

  git clone git@github.com:shaypal5/ssdts_matching.git


Install in development mode with test dependencies:

.. code-block:: bash

  cd ssdts_matching
  pip install -e ".[test]"


Running the tests
-----------------

To run the tests, use:

.. code-block:: bash

  python -m pytest --cov=ssdts_matching


Adding documentation
--------------------

This project is documented using the `numpy docstring conventions`_, which were chosen as they are perhaps the most widely-spread conventions that are both supported by common tools such as Sphinx and result in human-readable docstrings (in my personal opinion, of course). When documenting code you add to this project, please follow `these conventions`_.

.. _`numpy docstring conventions`: https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt
.. _`these conventions`: https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt


Credits
=======
Created by Shay Palachy  (shay.palachy@gmail.com).


.. |PyPI-Status| image:: https://img.shields.io/pypi/v/ssdts_matching.svg
  :target: https://pypi.python.org/pypi/ssdts_matching

.. |PyPI-Versions| image:: https://img.shields.io/pypi/pyversions/ssdts_matching.svg
   :target: https://pypi.python.org/pypi/ssdts_matching

.. |Build-Status| image:: https://travis-ci.org/shaypal5/ssdts_matching.svg?branch=master
  :target: https://travis-ci.org/shaypal5/ssdts_matching

.. |LICENCE| image:: https://img.shields.io/pypi/l/ssdts_matching.svg
  :target: https://pypi.python.org/pypi/ssdts_matching

.. |Codecov| image:: https://codecov.io/github/shaypal5/ssdts_matching/coverage.svg?branch=master
   :target: https://codecov.io/github/shaypal5/ssdts_matching?branch=master
