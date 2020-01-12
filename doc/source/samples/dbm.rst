==============
 DBM Samples
==============

Creating Data File
==================

.. include:: ../sample-data/make_dbm.py
   :literal:

Template File
=============

.. include:: /_templates/dbm-sample.tmpl
   :literal:

Loading the Template
====================

.. code-block:: rst

   .. datatemplate:dbm:: ../sample-data/sampledbm
      :template: dbm-sample.tmpl

Rendered Output
===============

.. datatemplate:dbm:: ../sample-data/sampledbm
   :template: dbm-sample.tmpl
