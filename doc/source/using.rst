====================
 Using datatemplate
====================

The ``datatemplate`` directive is the interface between the data
source and the rendering template.

.. rst:directive:: .. datatemplate:json:: source-path
    
   Load file at ``source-path`` (relative to the documentation build directory) via
   :py:func:`json.load` and render using ``template`` given in directive body.

   .. rst:directive:option:: template: template name, optional

        The name of a template file on the Sphinx template search path. Overrides directive body.
        
   .. rst:directive:option:: encoding: optional, defaults to ``utf-8-sig``

        The text encoding that will be used to read the source file. See :any:`standard-encodings`

.. rst:directive:: .. datatemplate:yaml:: source-path
    
   Load file at ``source-path`` (relative to the documentation build directory)  via 
   PyYAML_ (``yaml.safe_load``) and render using ``template`` given in directive body.

   .. rst:directive:option:: template: template name, optional

        The name of a template file on the Sphinx template search path. Overrides directive body.
        
   .. rst:directive:option:: encoding: optional, defaults to ``utf-8-sig``

        The text encoding that will be used to read the source file. See :any:`standard-encodings`

   .. rst:directive:option:: multiple-documents: flag, optional

        Set to read multiple documents from the file into a :py:class:`list`

.. _PyYAML: https://pyyaml.org

.. rst:directive:: .. datatemplate:xml:: source-path
    
   Load file at ``source-path`` (relative to the documentation build directory)  via
   :py:func:`xml.etree.ElementTree.parse` (actually using ``defusedxml``) and render using ``template`` given in directive body.

   .. rst:directive:option:: template: template name, optional

        The name of a template file on the Sphinx template search path. Overrides directive body.
        
.. rst:directive:: .. datatemplate:import-module:: module-name
    
   Load module ``module-name`` (must be importable in ``conf.py``)  via 
   :py:func:`importlib.import_module` and render using ``template`` given in directive body.

   .. rst:directive:option:: template: template name, optional

        The name of a template file on the Sphinx template search path. Overrides directive body.


.. rst:directive:: .. datatemplate:csv:: source-path
    
   Load file at ``source-path`` (relative to the documentation build directory) via
   :py:func:`csv.reader` or :py:class:`csv.DictReader` depending on ``header`` and render using ``template`` given in directive body.

   .. rst:directive:option:: template: template name, optional

        The name of a template file on the Sphinx template search path. Overrides directive body.
        
   .. rst:directive:option:: encoding: optional, defaults to ``utf-8-sig``

        The text encoding that will be used to read the source file. See :any:`standard-encodings`

   .. rst:directive:option:: header: flag, optional

        Set to use :py:class:`csv.DictReader` for reading the file.
        If not set :py:func:`csv.reader` is used.

   .. rst:directive:option:: dialect: either ``auto`` or one from :py:func:`csv.list_dialects`, optional

        Set to select a specific :py:class:`csv.Dialect`.
        Set to ``auto``, to try autodetection.
        If not set the default dialect is used.

.. rst:directive:: datatemplate:dbm:: source-path
    
   Load DB at ``source-path`` (relative to the documentation build directory)  via
   :py:func:`dbm.open` and render using ``template`` given in directive body.

   .. rst:directive:option:: template: template name, optional

        The name of a template file on the Sphinx template search path. Overrides directive body.
        

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
