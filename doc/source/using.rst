====================
 Using datatemplate
====================

The ``datatemplate`` directive is the interface between the data
source and the rendering template. It requires two parameters.

.. rst:directive:: datatemplate

   ``source``
      The source file, relative to the documentation build directory.

   ``template``
      The name of a template file on the Sphinx template search path.

Template Context
================

When a ``datatemplate`` directive is processed, the data is passed to
the template through its context so that the symbol ``data`` is
available as a global variable.

The data is loaded from the source and passed directly to the
template. No pre-processing is done on the data, so the template needs
to handle aspects like ``None`` values and fields that have values
that may interfere with parsing reStructuredText.

Template Helpers
================

These helper functions are exposed using their short name (without the
module prefix) in the template context.

.. automodule:: sphinxcontrib.datatemplates.helpers
   :members:
