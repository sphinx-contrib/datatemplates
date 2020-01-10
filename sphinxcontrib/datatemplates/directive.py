import json
import csv
import defusedxml.ElementTree as ET
import yaml
import dbm
import contextlib
import importlib
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


class DataTemplateBase(rst.Directive):

    _default_templates = None
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        'source': rst.directives.unchanged,
        'template': rst.directives.unchanged,
    }
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

    def _load_data(self, resolved_path):
        return NotImplemented

    @contextlib.contextmanager
    def _load_data_cm(self, resolved_path):
        yield self._load_data(resolved_path)

    def _resolve_source_path(self, env, data_source):
        rel_filename, filename = env.relfn2path(data_source)
        return filename

    def _make_context(self, data):
        return {
            'make_list_table': helpers.make_list_table,
            'make_list_table_from_mappings':
            helpers.make_list_table_from_mappings,
            'data': data,
        }

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


class DataTemplateWithEncoding(DataTemplateBase):
    option_spec = dict(DataTemplateBase.option_spec, **{
        'encoding': rst.directives.unchanged,
    })


class DataTemplateJSON(DataTemplateWithEncoding):
    def _load_data(self, resolved_path):
        with open(resolved_path,
                  'r',
                  encoding=self.options.get('encoding', 'utf-8-sig')) as f:
            return json.load(f)


def _handle_dialect_option(argument):
    return rst.directives.choice(argument, ["auto"] + csv.list_dialects())


class DataTemplateCSV(DataTemplateWithEncoding):
    option_spec = dict(
        DataTemplateBase.option_spec, **{
            'headers': rst.directives.flag,
            'dialect': _handle_dialect_option,
        })

    def _load_data(self, resolved_path):
        with open(resolved_path,
                  'r',
                  newline='',
                  encoding=self.options.get('encoding', 'utf-8-sig')) as f:
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


class DataTemplateYAML(DataTemplateWithEncoding):
    option_spec = dict(DataTemplateBase.option_spec, **{
        'multiple-documents': rst.directives.flag,
    })

    def _load_data(self, resolved_path):
        with open(resolved_path,
                  'r',
                  encoding=self.options.get('encoding', 'utf-8-sig')) as f:
            if 'multiple-documents' in self.options:
                return list(
                    yaml.safe_load_all(f)
                )  # force loading all documents now so the file can be closed
            return yaml.safe_load(f)


class DataTemplateXML(DataTemplateBase):
    def _load_data(self, resolved_path):
        return ET.parse(resolved_path).getroot()


class DataTemplateDBM(DataTemplateBase):
    def _load_data_cm(self, resolved_path):
        return dbm.open(resolved_path, "r")


class DataTemplateImportModule(DataTemplateBase):
    def _resolve_source_path(self, env, data_source):
        return data_source

    def _load_data(self, resolved_path):
        return importlib.import_module(resolved_path)
