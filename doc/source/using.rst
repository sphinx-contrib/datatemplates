====================
 Using datatemplate
====================

The ``datatemplate`` directive is the interface between the data
source and the rendering template. It requires two parameters.

.. rst:directive:: datatemplate:json
    
   Load ``source`` via :py:func:`json.load`

   .. rst:directive:option:: source: source path, required

        The source file, relative to the documentation build directory.

   .. rst:directive:option:: template: template name, required

        The name of a template file on the Sphinx template search path.
        
   .. rst:directive:option:: encoding: optional, defaults to ``utf-8-sig``

        The text encoding that will be used to read the source file. See :any:`standard-encodings`

.. rst:directive:: datatemplate:yaml
    
   Load ``source`` via PyYAML_ (``yaml.safe_load``)

   .. rst:directive:option:: source: source path, required

        The source file, relative to the documentation build directory.

   .. rst:directive:option:: template: template name, required

        The name of a template file on the Sphinx template search path.
        
   .. rst:directive:option:: encoding: optional, defaults to ``utf-8-sig``

        The text encoding that will be used to read the source file. See :any:`standard-encodings`

   .. rst:directive:option:: multiple-documents: flag, optional

        Set to read multiple documents from the file into a :py:class:`list`

.. _PyYAML: https://pyyaml.org

.. rst:directive:: datatemplate:xml
    
   Load ``source`` via :py:func:`xml.etree.ElementTree.parse` (actually using ``defusedxml``)

   .. rst:directive:option:: source: source path, required

        The source file, relative to the documentation build directory.

   .. rst:directive:option:: template: template name, required

        The name of a template file on the Sphinx template search path.
        
.. rst:directive:: datatemplate:import-module
    
   Load ``source`` via :py:func:`importlib.import_module`

   .. rst:directive:option:: source: module name, required

        Name of the module to import, must be importable in ``conf.py``

   .. rst:directive:option:: template: template name, required

        The name of a template file on the Sphinx template search path.


.. rst:directive:: datatemplate:csv
    
   Load ``source`` via :py:func:`csv.reader` or :py:class:`csv.DictReader` depending on ``header``

   .. rst:directive:option:: source: source path, required

        The source file, relative to the documentation build directory.

   .. rst:directive:option:: template: template name, required

        The name of a template file on the Sphinx template search path.
        
   .. rst:directive:option:: encoding: optional, defaults to ``utf-8-sig``

        The text encoding that will be used to read the source file. See :any:`standard-encodings`

   .. rst:directive:option:: header: flag, optional

        Set to use :py:class:`csv.DictReader` for reading the file.
        If not set :py:func:`csv.reader` is used.

   .. rst:directive:option:: dialect: either ``auto`` or one from :py:func:`csv.list_dialects`, optional

        Set to select a specific :py:class:`csv.Dialect`.
        Set to ``auto``, to try autodetection.
        If not set the default dialect is used.

.. rst:directive:: datatemplate:dbm
    
   Load ``source`` via :py:func:`dbm.open`

   .. rst:directive:option:: source: source path, required

        The source file (without extension), relative to the documentation build directory.

   .. rst:directive:option:: template: template name, required

        The name of a template file on the Sphinx template search path.
        

Template Context
================

When a ``datatemplate`` directive is processed, the data is passed to
the template through its context so that the symbol ``data`` is
available as a global variable.

.. important::
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
