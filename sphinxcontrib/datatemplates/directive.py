from docutils import nodes
from docutils.parsers import rst
from docutils.statemachine import ViewList
from sphinx.jinja2glue import BuiltinTemplateLoader
from sphinx.util import logging
from sphinx.util.nodes import nested_parse_with_titles

from . import mixins

LOG = logging.getLogger(__name__)


class DataTemplateDirective(rst.Directive):

    _default_templates = None
    optional_arguments = 1
    final_argument_whitespace = True
    has_content = True

    @classmethod
    def _templates(cls, env):
        app = env.app
        builder = app.builder

        # Some builders have no templates manager at all, and some
        # have the attribute set to None.
        templates = getattr(builder, 'templates', None)

        if not templates:
            if cls._default_templates is None:
                # Initialize default templates manager once
                _default_templates = BuiltinTemplateLoader()
                _default_templates.init(builder)
                cls._default_templates = _default_templates

            templates = cls._default_templates

        return templates

    def _resolve_source_path(self, env, data_source):
        _, filename = env.relfn2path(data_source)
        return filename

    def run(self):
        env = self.state.document.settings.env

        if 'source' in self.options:
            data_source = self.options['source']
        else:
            data_source = self.arguments[0]

        resolved_path = self._resolve_source_path(env, data_source)

        if 'template' in self.options:
            template = self.options['template']
            render_function = self._templates(env).render
        else:
            template = '\n'.join(self.content)
            render_function = self._templates(env).render_string

        with self._load_data_cm(resolved_path) as data:
            context = self._make_context(data)
            rendered_template = render_function(
                template,
                context,
            )

        result = ViewList()
        for line in rendered_template.splitlines():
            result.append(line, data_source)
        node = nodes.section()
        node.document = self.state.document
        nested_parse_with_titles(self.state, result, node)
        return node.children

    @classmethod
    def usage(cls):
        _, sep, doc = cls.__doc__.partition(".. rst:directive::")
        return sep + doc


class DataTemplateJSONDirective(mixins.DataTemplateJSON,
                                DataTemplateDirective):
    """
    .. rst:directive:: .. datatemplate:json:: source-path
    
        Load file at ``source-path`` (relative to the documentation build directory) via
        :py:func:`json.load` and render using ``template`` given in directive body.

        .. rst:directive:option:: template: template name, optional

            The name of a template file on the Sphinx template search path. Overrides directive body.
            
        .. rst:directive:option:: encoding: optional, defaults to ``utf-8-sig``

            The text encoding that will be used to read the source file. See :any:`standard-encodings`
    """


class DataTemplateCSVDirective(mixins.DataTemplateCSV, DataTemplateDirective):
    """
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
    """


class DataTemplateYAMLDirective(mixins.DataTemplateYAML,
                                DataTemplateDirective):
    """
    .. rst:directive:: .. datatemplate:yaml:: source-path
            
        Load file at ``source-path`` (relative to the documentation build directory)  via 
        PyYAML_ (:py:func:`yaml.safe_load`) and render using ``template`` given in directive body.

        .. rst:directive:option:: template: template name, optional

                The name of a template file on the Sphinx template search path. Overrides directive body.
                
        .. rst:directive:option:: encoding: optional, defaults to ``utf-8-sig``

                The text encoding that will be used to read the source file. See :any:`standard-encodings`

        .. rst:directive:option:: multiple-documents: flag, optional

                Set to read multiple documents from the file into a :py:class:`list`

    .. _PyYAML: https://pyyaml.org
    """


class DataTemplateXMLDirective(mixins.DataTemplateXML, DataTemplateDirective):
    """
    .. rst:directive:: .. datatemplate:xml:: source-path
    
        Load file at ``source-path`` (relative to the documentation build directory)  via
        :py:func:`xml.etree.ElementTree.parse` (actually using ``defusedxml``) and render using ``template`` given in directive body.

        .. rst:directive:option:: template: template name, optional

                The name of a template file on the Sphinx template search path. Overrides directive body.
    """


class DataTemplateDBMDirective(mixins.DataTemplateDBM, DataTemplateDirective):
    """
    .. rst:directive:: datatemplate:dbm:: source-path
    
        Load DB at ``source-path`` (relative to the documentation build directory)  via
        :py:func:`dbm.open` and render using ``template`` given in directive body.

        .. rst:directive:option:: template: template name, optional

                The name of a template file on the Sphinx template search path. Overrides directive body.
    """


class DataTemplateImportModuleDirective(mixins.DataTemplateImportModule,
                                        DataTemplateDirective):
    """
    .. rst:directive:: .. datatemplate:import-module:: module-name
        
        Load module ``module-name`` (must be importable in ``conf.py``)  via 
        :py:func:`importlib.import_module` and render using ``template`` given in directive body.

        .. rst:directive:option:: template: template name, optional

                The name of a template file on the Sphinx template search path. Overrides directive body.
    """
