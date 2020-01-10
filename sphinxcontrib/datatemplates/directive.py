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


class DataTemplateJSONDirective(mixins.DataTemplateJSON,
                                DataTemplateDirective):
    pass


class DataTemplateCSVDirective(mixins.DataTemplateCSV, DataTemplateDirective):
    pass


class DataTemplateYAMLDirective(mixins.DataTemplateYAML,
                                DataTemplateDirective):
    pass


class DataTemplateXMLDirective(mixins.DataTemplateXML, DataTemplateDirective):
    pass


class DataTemplateDBMDirective(mixins.DataTemplateDBM, DataTemplateDirective):
    pass


class DataTemplateImportModuleDirective(mixins.DataTemplateImportModule,
                                        DataTemplateDirective):
    pass
