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


class AbstractDataTemplateBase:
    option_spec = {
        'source': rst.directives.unchanged,
        'template': rst.directives.unchanged,
    }

    def _load_data(self, resolved_path):
        return NotImplemented

    @contextlib.contextmanager
    def _load_data_cm(self, resolved_path):
        yield self._load_data(resolved_path)

    def _make_context(self, data):
        return {
            'make_list_table': helpers.make_list_table,
            'make_list_table_from_mappings':
            helpers.make_list_table_from_mappings,
            'data': data,
        }


class AbstractDataTemplateWithEncoding(AbstractDataTemplateBase):
    option_spec = dict(
        AbstractDataTemplateBase.option_spec, **{
            'encoding':
            (lambda s: 'utf-8-sig' if s is None else rst.directives.encoding),
        })


class DataTemplateJSON(AbstractDataTemplateWithEncoding):
    def _load_data(self, resolved_path):
        with open(resolved_path, 'r', encoding=self.options['encoding']) as f:
            return json.load(f)


def _handle_dialect_option(argument):
    return rst.directives.choice(argument, ["auto"] + csv.list_dialects())


class DataTemplateCSV(AbstractDataTemplateWithEncoding):
    option_spec = dict(
        AbstractDataTemplateBase.option_spec, **{
            'headers': rst.directives.flag,
            'dialect': _handle_dialect_option,
        })

    def _load_data(self, resolved_path):
        with open(resolved_path,
                  'r',
                  newline='',
                  encoding=self.options['encoding']) as f:
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


class DataTemplateYAML(AbstractDataTemplateWithEncoding):
    option_spec = dict(AbstractDataTemplateBase.option_spec, **{
        'multiple-documents': rst.directives.flag,
    })

    def _load_data(self, resolved_path):
        with open(resolved_path, 'r', encoding=self.options['encoding']) as f:
            if 'multiple-documents' in self.options:
                return list(
                    yaml.safe_load_all(f)
                )  # force loading all documents now so the file can be closed
            return yaml.safe_load(f)


class DataTemplateXML(AbstractDataTemplateBase):
    def _load_data(self, resolved_path):
        return ET.parse(resolved_path).getroot()


class DataTemplateDBM(AbstractDataTemplateBase):
    def _load_data_cm(self, resolved_path):
        return dbm.open(resolved_path, "r")


class DataTemplateImportModule(AbstractDataTemplateBase):
    def _resolve_source_path(self, env, data_source):
        return data_source

    def _load_data(self, resolved_path):
        return importlib.import_module(resolved_path)