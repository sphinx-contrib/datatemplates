.. -*- mode: rst -*-

=============================
 sphinxcontrib-datatemplates
=============================

This package contains sphinxcontrb.datatemplates, an extension for
Sphinx to render parts of reStructuredText pages from data files in
formats like JSON, YAML, and CSV.

* Repo: https://github.com/sphinxcontrib/sphinxcontrib.datatemplates
* Docs: http://sphinxcontribdatatemplates.readthedocs.io/

Sample YAML Input
=================

::

    ---
    key1: value1
    key2:
      - list item 1
      - list item 2
      - list item 3
    nested-list:
      - ['a', 'b', 'c']
      - ['A', 'B', 'C']
    mapping-series:
      - cola: a
        colb: b
        colc: c
      - cola: A
        colb: B
        colc: C

Sample Template
===============

::

    .. -*- mode: rst -*-
    
    Individual Item
    ~~~~~~~~~~~~~~~
    
    {{ data['key1'] }}
    
    List of Items
    ~~~~~~~~~~~~~
    
    {% for item in data['key2'] %}
    - {{item}}
    {% endfor %}
    
    Nested List Table
    ~~~~~~~~~~~~~~~~~
    
    Rendering a table from a list of nested sequences using hard-coded
    headers.
    
    {{ make_list_table(
        ['One', 'Two', 'Three'],
        data['nested-list'],
        title='Table from nested lists',
        ) }}
    
    Mapping Series Table
    ~~~~~~~~~~~~~~~~~~~~
    
    Rendering a table from a list of nested dictionaries using dynamic
    headers.
    
    {{ make_list_table_from_mappings(
        [('One', 'cola'), ('Two', 'colb'), ('Three', 'colc')],
        data['mapping-series'],
        title='Table from series of mappings',
        ) }}

Rendered Output
===============

See the `sphinx output
<https://sphinxcontribdatatemplates.readthedocs.io/en/latest/yaml.html#rendered-output>`_ online.
