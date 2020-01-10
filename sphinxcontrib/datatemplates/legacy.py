import json
import csv
import defusedxml.ElementTree as ET
import yaml
import mimetypes
import codecs

from docutils import nodes
from docutils.parsers import rst
from docutils.statemachine import ViewList
from sphinx.jinja2glue import BuiltinTemplateLoader
from sphinx.util import logging
from sphinx.util.nodes import nested_parse_with_titles

from sphinxcontrib.datatemplates import helpers

LOG = logging.getLogger(__name__)
_default_templates = None


def _templates(builder):
    global _default_templates

    # Some builders have no templates manager at all, and some
    # have the attribute set to None.
    templates = getattr(builder, 'templates', None)

    if not templates:
        if not _default_templates:
            # Initialize default templates manager once
            _default_templates = BuiltinTemplateLoader()
            _default_templates.init(builder)

        templates = _default_templates

    return templates


def _handle_dialect_option(argument):
    return rst.directives.choice(argument, ["auto"] + csv.list_dialects())


class DataTemplateLegacy(rst.Directive):

    option_spec = {
        'source': rst.directives.unchanged,
        'template': rst.directives.unchanged,
        'csvheaders': rst.directives.flag,
        'csvdialect': _handle_dialect_option,
        'encoding': rst.directives.unchanged,
    }
    has_content = False

    def _load_csv(self, filename, encoding):
        try:
            if encoding is None:
                f = open(filename, 'r', newline='')
            else:
                f = codecs.open(filename, 'r', newline='', encoding=encoding)
            dialect = self.options.get('csvdialect')
            if dialect == "auto":
                sample = f.read(8192)
                f.seek(0)
                sniffer = csv.Sniffer()
                dialect = sniffer.sniff(sample)
            if 'csvheaders' in self.options:
                if dialect is None:
                    r = csv.DictReader(f)
                else:
                    r = csv.DictReader(f, dialect=dialect)
            else:
                if dialect is None:
                    r = csv.reader(f)
                else:
                    r = csv.reader(f, dialect=dialect)
            return list(r)
        finally:
            f.close()

    def _load_json(self, filename, encoding):
        try:
            if encoding is None:
                f = open(filename, 'r')
            else:
                f = codecs.open(filename, 'r', encoding=encoding)
            return json.load(f)
        finally:
            f.close()

    def _load_yaml(self, filename, encoding):
        try:
            if encoding is None:
                f = open(filename, 'r')
            else:
                f = codecs.open(filename, 'r', encoding=encoding)
            return yaml.safe_load(f)
        finally:
            f.close()

    def _load_data(self, env, data_source, encoding):
        rel_filename, filename = env.relfn2path(data_source)
        if data_source.endswith('.yaml'):
            return self._load_yaml(filename, encoding)
        elif data_source.endswith('.json'):
            return self._load_json(filename, encoding)
        elif data_source.endswith('.csv'):
            return self._load_csv(filename, encoding)
        elif "xml" in mimetypes.guess_type(data_source)[0]:
            # there are many XML based formats
            return ET.parse(filename).getroot()
        else:
            raise NotImplementedError('cannot load file type of %s' %
                                      data_source)

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

        encoding = self.options.get('encoding', None)

        data = self._load_data(env, data_source, encoding)

        context = {
            'make_list_table': helpers.make_list_table,
            'make_list_table_from_mappings':
            helpers.make_list_table_from_mappings,
            'data': data,
        }
        rendered_template = _templates(builder).render(
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