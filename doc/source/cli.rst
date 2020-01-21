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

   python -m sphinxcontrib.datatemplates.cli -o multiple-documents:1  doc/source/_templates/sample-multiple.tmpl doc/source/sample-multiple.yaml

Output
======

.. runcmd:: python -m sphinxcontrib.datatemplates.cli -o multiple-documents:1  doc/source/_templates/sample-multiple.tmpl doc/source/sample-multiple.yaml
