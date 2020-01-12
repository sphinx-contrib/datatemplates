======================
 Inline Sample (JSON)
======================

Data File
=========

.. include:: sample-data/sample.json
   :literal:

Template File
=============

.. code-block:: jinja
   
      Individual Item
      ~~~~~~~~~~~~~~~

      {{ data['key1'] }}

      List of Items
      ~~~~~~~~~~~~~

      {% for item in data['key2'] %}
      - {{item}}
      {% endfor %}

Loading the Template
====================

.. code-block:: rst

   .. datatemplate:json::
      :source: sample-data/sample.json
      
      Individual Item
      ~~~~~~~~~~~~~~~

      {{ data['key1'] }}

      List of Items
      ~~~~~~~~~~~~~

      {% for item in data['key2'] %}
      - {{item}}
      {% endfor %}

Rendered Output
===============

.. datatemplate:json::
   :source: sample-data/sample.json
   
   Individual Item
   ~~~~~~~~~~~~~~~
   
   {{ data['key1'] }}

   List of Items
   ~~~~~~~~~~~~~

   {% for item in data['key2'] %}
   - {{item}}
   {% endfor %}
