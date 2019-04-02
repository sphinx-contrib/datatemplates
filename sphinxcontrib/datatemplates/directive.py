import json

from docutils import nodes
from docutils.parsers import rst
from docutils.statemachine import ViewList
from sphinx.util import logging
from sphinx.util.nodes import nested_parse_with_titles
import yaml

from sphinxcontrib.datatemplates import helpers

LOG = logging.getLogger(__name__)


class DataTemplate(rst.Directive):

    option_spec = {
        'source': rst.directives.unchanged,
        'template': rst.directives.unchanged,
    }
    has_content = False

    def _load_data(self, env, data_source):
        rel_filename, filename = env.relfn2path(data_source)
        if data_source.endswith('.yaml'):
            with open(filename, 'r') as f:
                return yaml.load(f)
        elif data_source.endswith('.json'):
            with open(filename, 'r') as f:
                return json.load(f)
        else:
            raise NotImplementedError('cannot load file type of %s' %
                                      data_source)

    def run(self):
        env = self.state.document.settings.env
        app = env.app
        builder = app.builder
        # Some builders have no templates manager at all, and some
        # have the attribute set to None.
        templates = getattr(builder, 'templates', None)
        if not templates:
            LOG.warn(
                'The builder has no template manager, '
                'ignoring the datatemplate directive.')
            return []

        try:
            data_source = self.options['source']
        except KeyError:
            error = self.state_machine.reporter.error(
                'No source set for datatemplate directive',
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno)
            return [error]

        try:
            template_name = self.options['template']
        except KeyError:
            error = self.state_machine.reporter.error(
                'No template set for datatemplate directive',
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno)
            return [error]

        data = self._load_data(env, data_source)

        context = {
            'make_list_table': helpers.make_list_table,
            'make_list_table_from_mappings':
                helpers.make_list_table_from_mappings,
            'data': data,
        }
        rendered_template = builder.templates.render(
            template_name,
            context,
        )

        result = ViewList()
        for line in rendered_template.splitlines():
            result.append(line, data_source)
        node = nodes.section()
        node.document = self.state.document
        nested_parse_with_titles(self.state, result, node)
        return node.children
