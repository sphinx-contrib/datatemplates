=======================
 Multiple Data Sources
=======================

Data Files
==========

Part details, indexed by a part number:

.. include:: part-details.yaml
   :literal:

Inventory counts:

.. include:: inventory.csv
   :literal:

Using ``load()`` in a Template
==============================

The ``load()`` function visible in the template context can be used to
load static data sources.

.. literalinclude:: _templates/inventory.tmpl
   :language: rst

``load()`` will attempt to guess the format for a data source based on
the name by looking at file extensions. To explicitly select a format,
pass the name in the ``data_format`` argument.

.. code-block:: rst

   {% set parts = load('part-details.dat', data_format='yaml') %}

The arguments given to the ``datatemplate`` directive are also passed
to the loader used by ``load()``. To override those settings, or
provide different values for a different format, pass the arguments
directly to ``load()``.

.. code-block:: rst

   {% set parts = load('part-details.dat', data_format='json', encoding='UTF-8') %}

.. note::

   Database formats like ``dbm`` are not supported, and should be used
   as the primary data source for a ``datatemplate`` directive.

Loading the Template
====================

.. code-block:: rst

   .. datatemplate:csv:: inventory.csv
      :template: inventory.tmpl

Rendered Output
===============

.. datatemplate:csv:: inventory.csv
   :template: inventory.tmpl
