========================================
 Installing sphinxcontrib.datatemplates
========================================

Install ``sphinxcontrib.datatemplates`` into the Python environment
where Sphinx is installed.

.. code-block:: console

   $ pip install sphinxcontrib.datatemplates

Then modify the ``conf.py`` for the Sphinx project to add the package
to the list of active extensions.

.. code-block:: python

   extensions = [
       'sphinxcontrib.datatemplates',
   ]
