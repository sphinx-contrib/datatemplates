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

Code
=====

.. code-block:: rst

    .. datatemplate-csv::
        :source: sample.csv
        :template: csv-sample.tmpl
        :headers:
        :dialect: excel-tab

Rendered Output
===============

.. datatemplate-csv::
    :source: sample.csv
    :template: csv-sample.tmpl
    :headers:
    :dialect: excel-tab
