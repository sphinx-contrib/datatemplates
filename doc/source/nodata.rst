================
 No Data Sample
================


Loading the Template
====================

.. code-block:: rst

   .. datatemplate:nodata::

      Inline data:

      - {{ data }}

      Document titles from the Sphinx environment:

      {% for doc, title in env.titles.items() %}
      - ``{{ title }} ({{ doc }})``
      {% endfor %}


Rendered Output
===============

.. datatemplate:nodata::

    Inline data:

   - {{ data }}

   Document titles from the Sphinx environment:

   {% for doc, title in env.titles.items() %}
   - ``{{ title }} ({{ doc }})``
   {% endfor %}
