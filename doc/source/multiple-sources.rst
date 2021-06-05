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

Template File
=============

.. include:: _templates/inventory.tmpl
   :literal:

Loading the Template
====================

.. code-block:: rst

   .. datatemplate:csv:: inventory.csv
      :template: inventory.tmpl

Rendered Output
===============

.. datatemplate:csv:: inventory.csv
   :template: inventory.tmpl
