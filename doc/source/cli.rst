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

Output
------

.. runcmd:: datatemplate render -o multiple-documents  doc/source/_templates/sample-multiple.tmpl doc/source/sample-multiple.yaml
