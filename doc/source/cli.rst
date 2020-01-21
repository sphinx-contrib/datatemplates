==============
 CLI Samples
==============

Help
====

.. runcmd:: python -m sphinxcontrib.datatemplates.cli --help

Data File
=========

.. include:: sample-multiple.yaml
   :literal:

Template File
=============

.. include:: _templates/sample-multiple.tmpl
   :literal:

Command Line
============

.. code-block:: bat

   python -m sphinxcontrib.datatemplates.cli doc/source/sample-multiple.yaml doc/source/_templates/sample-multiple.tmpl --option multiple-documents:1

Output
======

.. runcmd:: python -m sphinxcontrib.datatemplates.cli doc/source/sample-multiple.yaml doc/source/_templates/sample-multiple.tmpl --option multiple-documents:1
