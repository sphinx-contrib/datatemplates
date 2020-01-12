===================
Command Line Usage
===================


.. datatemplate:import-module:: sphinxcontrib.datatemplates.standalone

    {% for name in data.datatemplate_names|sort() %}
    .. autoprogram:: sphinxcontrib.datatemplates.standalone:doc_main_{{name.replace("-","_")}}()
        :prog: datatemplate-{{name}}

    {% endfor %}

