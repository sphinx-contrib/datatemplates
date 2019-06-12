import json
import csv
import mimetypes

import defusedxml.ElementTree as ET
import yaml
from docutils import nodes
from docutils.parsers import rst
from docutils.statemachine import ViewList
from sphinx.util import logging
from sphinx.util.nodes import nested_parse_with_titles

from sphinxcontrib.datatemplates import helpers

LOG = logging.getLogger(__name__)


class DataTemplateBase(rst.Directive):

    option_spec = {
        'source': rst.directives.unchanged_required,
        'template': rst.directives.unchanged_required,
    }
    has_content = False

    def _load_data(self, resolved_path):
        return NotImplemented

    def _resolve_source_path(self, env, data_source):
        rel_filename, filename = env.relfn2path(data_source)
        return filename

    def run(self):
        env = self.state.document.settings.env
        app = env.app
        builder = app.builder
        # Some builders have no templates manager at all, and some
        # have the attribute set to None.
        templates = getattr(builder, 'templates', None)
        if not templates:
            LOG.warn('The builder has no template manager, '
                     'ignoring the datatemplate directive.')
            return []

        data_source = self.options['source']
        template_name = self.options['template']

        resolved_path = self._resolve_source_path(env, data_source)
        data = self._load_data(resolved_path)

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


class DataTemplateJSON(DataTemplateBase):
    def _load_data(self, resolved_path):
        with open(resolved_path, 'r') as f:
            return json.load(f)


def _handle_dialect_option(argument):
    return rst.directives.choice(argument, ["auto"] + csv.list_dialects())


class DataTemplateCSV(DataTemplateBase):
    option_spec = dict(
        DataTemplateBase.option_spec, **{
            'headers': rst.directives.flag,
            'dialect': _handle_dialect_option,
        })

    def _load_data(self, resolved_path):
        with open(resolved_path, 'r', newline='') as f:
            dialect = self.options.get('dialect')
            if dialect == "auto":
                sample = f.read(8192)
                f.seek(0)
                sniffer = csv.Sniffer()
                dialect = sniffer.sniff(sample)
            if 'headers' in self.options:
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


class DataTemplateYAML(DataTemplateBase):
    def _load_data(self, resolved_path):
        with open(resolved_path, 'r') as f:
            return yaml.safe_load(f)


class DataTemplateXML(DataTemplateBase):
    def _load_data(self, resolved_path):
        return ET.parse(resolved_path).getroot()


class DataTemplateLegacy(rst.Directive):

    option_spec = {
        'source': rst.directives.unchanged,
        'template': rst.directives.unchanged,
        'csvheaders': rst.directives.flag,
        'csvdialect': _handle_dialect_option,
    }
    has_content = False

    def _load_data(self, env, data_source):
        rel_filename, filename = env.relfn2path(data_source)
        if data_source.endswith('.yaml'):
            with open(filename, 'r') as f:
                return yaml.safe_load(f)
        elif data_source.endswith('.json'):
            with open(filename, 'r') as f:
                return json.load(f)
        elif data_source.endswith('.csv'):
            with open(filename, 'r', newline='') as f:
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
        elif "xml" in mimetypes.guess_type(data_source)[0]:
            return ET.parse(filename).getroot()

        else:
            raise NotImplementedError('cannot load file type of %s' %
                                      data_source)

    def run(self):
        LOG.warning('Using the datatemplate directive is deprecated. '
                    'Please use one of the format-specific variants.')
        env = self.state.document.settings.env
        app = env.app
        builder = app.builder
        # Some builders have no templates manager at all, and some
        # have the attribute set to None.
        templates = getattr(builder, 'templates', None)
        if not templates:
            LOG.warn('The builder has no template manager, '
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
