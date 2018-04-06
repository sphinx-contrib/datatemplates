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

   ``key``
      **Optional**: A specific data key to pass to the template, so you can render a subset of the data.

   ``include_env``
      **Optional**: A flag that includes the ``env`` from your Sphinx in the _template_ rendering context.

   ``include_context``
      **Optional**: A flag that includes the ``env.app.config.html_context`` from your Sphinx in the _template_ rendering context. This could overwrite existing template context!

Template Context
================

When a ``datatemplate`` directive is processed, the data is passed to
the template through its context so that the symbol ``data`` is
available as a global variable.

The data is loaded from the source and passed directly to the
template. No pre-processing is done on the data, so the template needs
to handle aspects like ``None`` values and fields that have values
that may interfere with parsing reStructuredText.

If you set ``:key: foo`` on the directive,
you will have a top-level ``key`` variable.
This can be used to render a subset of the data in the template.

If you set `:include_context:` on the directive,
your template have the full ``env.app.config.html_context`` injected at the top-level.
This allows you to maintain Jinja templates that work for both rendering in normal Sphinx builds,
and within datatemplates.

If you set `:include_env:` on the directive,
your template will also have access to the builder's ``env`` while rendering.
This gives you more flexibility,
but is not as user friendly as `:include_context:`.

An example would look like::

    .. datatemplate::
       :source: all-videos.yaml
       :template: video-listing.jinja
       :key: keynote-1
       :include_context:


Template Helpers
================

These helper functions are exposed using their short name (without the
module prefix) in the template context.

.. automodule:: sphinxcontrib.datatemplates.helpers
   :members:
