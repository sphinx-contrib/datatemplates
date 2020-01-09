==============
 CSV Samples
==============

Data File
=========

.. literalinclude:: sample.csv
   :language: text


Template File
=============

.. literalinclude:: _templates/csv-sample.tmpl
   :language: jinja

Loading the Template
====================

.. code-block:: rst

    .. datatemplate:csv:: sample.csv
        :template: csv-sample.tmpl
        :headers:
        :dialect: excel-tab

Rendered Output
===============

.. datatemplate:csv:: sample.csv
    :template: csv-sample.tmpl
    :headers:
    :dialect: excel-tab
