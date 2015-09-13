from docutils import nodes
from docutils.parsers import rst
from docutils.statemachine import ViewList
from sphinx.util.nodes import nested_parse_with_titles
import yaml


class DataTemplate(rst.Directive):

    option_spec = {
        'source': rst.directives.unchanged,
        'template': rst.directives.unchanged,
    }
    has_content = False

    def run(self):
        env = self.state.document.settings.env
        app = env.app
        builder = app.builder

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

        rel_filename, filename = env.relfn2path(data_source)
        if data_source.endswith('.yaml'):
            with open(filename, 'r') as f:
                data = yaml.load(f)
        else:
            raise NotImplementedError('cannot load file type of %s' %
                                      data_source)

        context = {
            'data': data,
        }
        rendered_template = builder.templates.render(
            template_name,
            context,
        )
        print(rendered_template)

        result = ViewList()
        for line in rendered_template.splitlines():
            result.append(line, data_source)
        node = nodes.section()
        node.document = self.state.document
        nested_parse_with_titles(self.state, result, node)
        return node.children
