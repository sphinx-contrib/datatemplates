======================
 Inline Sample (JSON)
======================

This example demonstrates how to use an inline template, as well as
accessing the :ref:`HTML context <template_context>` available to all
``datatemplate`` directives.

Data File
=========

.. include:: sample.json
   :literal:

HTML Context
============

.. code-block:: python

   # from conf.py
   html_context = {
       'sample': 'Sample context value set in conf.py',
   }

Loading the Template
====================

.. code-block:: rst

   .. datatemplate:json::
      :source: sample.json

      Individual Item
      ~~~~~~~~~~~~~~~

      {{ data['key1'] }}

      List of Items
      ~~~~~~~~~~~~~

      {% for item in data['key2'] %}
      - {{item}}
      {% endfor %}

      HTML Context
      ~~~~~~~~~~~~

      {% for key, value in config.html_context.items() %}
      - ``{{key}}`` = ``{{value}}``
      {% endfor %}

Rendered Output
===============

.. datatemplate:json::
   :source: sample.json

   Individual Item
   ~~~~~~~~~~~~~~~

   {{ data['key1'] }}

   List of Items
   ~~~~~~~~~~~~~

   {% for item in data['key2'] %}
   - {{item}}
   {% endfor %}

   HTML Context
   ~~~~~~~~~~~~

   {% for key, value in config.html_context.items() %}
   - ``{{key}}`` = ``{{value}}``
   {% endfor %}
