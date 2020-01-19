====================
 Using datatemplate
====================

The ``datatemplate`` directive is the interface between the data
source and the rendering template.

Directives
==========

.. datatemplate:import-module::
      :source: sphinxcontrib.datatemplates.domain
      
      {% for key,directive in data.DataTemplateDomain.directives.items()|sort() %}
      {{directive.usage()}}

      {% endfor %}
        

.. _template_context:

Template Context
================

When a ``datatemplate`` directive is processed, the data from the
``source`` is passed to the template through its context so that the
symbol ``data`` is available as a global variable.

.. important::
    The data is loaded from the source and passed directly to the
    template. No pre-processing is done on the data, so the template needs
    to handle aspects like ``None`` values and fields that have values
    that may interfere with parsing reStructuredText.

If the `HTML context`_ is set for a project, it will be passed to the
template as the symbol ``html_context``. If the HTML context is
missing or empty, ``html_context`` will be an empty dictionary. Refer
to the :doc:`inline` for an example.

.. _HTML context: https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_context

Template Helpers
================

These helper functions are exposed using their short name (without the
module prefix) in the template context.

.. automodule:: sphinxcontrib.datatemplates.helpers
   :members:
