==============
 CLI Samples
==============

Help
====

.. runcmd:: datatemplate --help

Data File
=========

.. include:: sample-multiple.yaml
   :literal:

Template File
=============

.. include:: _templates/sample-multiple.tmpl
   :literal:

Rendering a Template
====================

.. code-block:: console

   $ datatemplate render -o multiple-documents \
     doc/source/_templates/sample-multiple.tmpl \
     doc/source/sample-multiple.yaml

.. runcmd:: datatemplate render -o multiple-documents  doc/source/_templates/sample-multiple.tmpl doc/source/sample-multiple.yaml

Experimenting by Dumping Data
=============================

CSV Data With Headers
---------------------

.. code-block:: console

   $ datatemplate dump -o dialect:excel-tab \
     -o headers \
     doc/source/sample.csv

.. runcmd:: datatemplate dump -o dialect:excel-tab -o headers doc/source/sample.csv

CSV Data Without Headers
------------------------

.. code-block:: console

   $ datatemplate dump -o dialect:excel-tab \
     doc/source/sample.csv

.. runcmd:: datatemplate dump -o dialect:excel-tab doc/source/sample.csv
