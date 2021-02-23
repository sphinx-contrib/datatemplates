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

Template Files
==============

The ``datatemplate`` directive uses Sphinx's `templates_path`_
configuration setting to search for template files.

.. _templates_path: https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-templates_path

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

The `application configuration`_ for a project will be passed to the
template as the symbol ``config``. This can be used, for example, to
access `HTML context`_ via ``config.html_context``. Refer to the
:doc:`inline` for an example.

The `Sphinx build environment`_ for a project will be passed to the
template as the symbol ``env``. This can be used to access all of the
information that Sphinx has about the current build, including
settings, and document names. Refer to the :doc:`nodata` for an example.

.. _HTML context: https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_context
.. _application configuration: https://www.sphinx-doc.org/en/master/usage/configuration.html
.. _Sphinx build environment: https://www.sphinx-doc.org/en/master/extdev/envapi.html#sphinx.environment.BuildEnvironment

Template Helpers
================

These helper functions are exposed using their short name (without the
module prefix) in the template context.

.. automodule:: sphinxcontrib.datatemplates.helpers
   :members:
