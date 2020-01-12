==============
 YAML Samples
==============

Single Document
+++++++++++++++

Data File
=========

.. include:: ../sample-data/sample.yaml
   :literal:

Template File
=============

.. include:: /_templates/sample.tmpl
   :literal:

Loading the Template
====================

.. code-block:: rst

   .. datatemplate:yaml:: ../sample-data/sample.yaml
      :template: sample.tmpl

Rendered Output
===============

.. datatemplate:yaml:: ../sample-data/sample.yaml
   :template: sample.tmpl


Multiple Documents
++++++++++++++++++


Data File
=========

.. include:: ../sample-data/sample-multiple.yaml
   :literal:

Template File
=============

.. include:: /_templates/sample-multiple.tmpl
   :literal:

Loading the Template
====================

.. code-block:: rst

   .. datatemplate:yaml:: ../sample-data/sample-multiple.yaml
      :template: sample-multiple.tmpl
      :multiple-documents:

Rendered Output
===============

.. datatemplate:yaml:: ../sample-data/sample-multiple.yaml
   :template: sample-multiple.tmpl
   :multiple-documents: