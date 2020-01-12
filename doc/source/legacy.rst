================
 Legacy Samples
================

The ``datatemplate`` directive is should no longer be used. It is
deprecated, and will be removed in the next release.

Data File
=========

.. include:: sample-data/sample.yaml
   :literal:

Template File
=============

.. include:: _templates/sample.tmpl
   :literal:

Rendered Output
===============

.. datatemplate::
   :source: sample-data/sample.yaml
   :template: sample.tmpl
