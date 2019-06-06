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

    .. datatemplate::
        :source: sample.csv
        :template: csv-sample.tmpl
        :csvheaders:
        :csvdialect: excel-tab

Rendered Output
===============

    .. datatemplate::
        :source: sample.csv
        :template: csv-sample.tmpl
        :csvheaders:
        :csvdialect: excel-tab
