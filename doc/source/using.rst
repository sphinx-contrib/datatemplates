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

   ``encoding`` optional, defaults to ``utf-8-sig``
      The text encoding that will be used to read the source file. See :any:`standard-encodings`


   ``csvheader`` optional flag, CSV only
      Set to use :py:class:`csv.DictReader` for reading the file.
      If not set :py:func:`csv.reader` is used.

   ``csvdialect`` optional, CSV only, either ``auto`` or one from :py:func:`csv.list_dialects`
      Set to select a specific :py:class:`csv.Dialect`.
      Set to ``auto``, to try autodetection.
      If not set the default dialect is used.

Template Context
================

When a ``datatemplate`` directive is processed, the data is passed to
the template through its context so that the symbol ``data`` is
available as a global variable.

.. list-table::
   :header-rows: 1

   - * Format
     * ``data`` type
   - * JSON
     * the object returned by ``json.safe_load()`` (varies based on
       input)
   - * YAML
     * the object returned by the PyYAML_ function ``yaml.safe_load()``
       (varies based on input)
   - * XML
     * :py:class:`xml.etree.ElementTree.ElementTree`
   - * CSV
     * ``list`` of ``tuple`` or ``dict`` (when ``csvheaders`` option
       is specified)

.. _PyYAML: https://pyyaml.org

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
