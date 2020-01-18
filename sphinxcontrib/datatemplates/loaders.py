import contextlib
import json
import yaml
import defusedxml.ElementTree as ET
import dbm
import importlib
import csv
import re
import mimetypes

registered_loaders = []


class LoaderEntry:
    def __init__(self, loader, name, match_source):
        self.loader = loader
        self.name = name
        if isinstance(match_source, str):
            self.match_source = re.compile(match_source).match
        else:
            self.match_source = match_source


def loader_for_source(source, default=None):
    for e in registered_loaders:
        if e.match_source(source):
            return e.loader
    return default


def loader_by_name(name, default=None):
    for e in registered_loaders:
        if e.name == name:
            return e.loader
    return default


@contextlib.contextmanager
def load_csv(source,
             absolute_resolved_path,
             headers=False,
             dialect=None,
             encoding='utf-8-sig',
             **options):
    with open(absolute_resolved_path, 'r', newline='', encoding=encoding) as f:
        if dialect == "auto":
            sample = f.read(8192)
            f.seek(0)
            sniffer = csv.Sniffer()
            dialect = sniffer.sniff(sample)
        if headers:
            if dialect is None:
                r = csv.DictReader(f)
            else:
                r = csv.DictReader(f, dialect=dialect)
        else:
            if dialect is None:
                r = csv.reader(f)
            else:
                r = csv.reader(f, dialect=dialect)
        yield list(r)


registered_loaders.append(LoaderEntry(load_csv, "csv", ".*?[.]csv$"))


@contextlib.contextmanager
def load_json(source, absolute_resolved_path, encoding='utf-8-sig', **options):
    with open(absolute_resolved_path, 'r', encoding=encoding) as f:
        yield json.load(f)


registered_loaders.append(LoaderEntry(load_json, "json", ".*?[.]json$"))


@contextlib.contextmanager
def load_yaml(source,
              absolute_resolved_path,
              encoding='utf-8-sig',
              multiple_documents=False,
              **options):
    with open(absolute_resolved_path, 'r', encoding=encoding) as f:
        if multiple_documents:
            yield list(
                yaml.safe_load_all(f)
            )  # force loading all documents now so the file can be closed
        else:
            yield yaml.safe_load(f)


registered_loaders.append(LoaderEntry(load_yaml, "yaml", ".*?[.]yaml$"))


@contextlib.contextmanager
def load_xml(source, absolute_resolved_path, **options):
    yield ET.parse(absolute_resolved_path).getroot()


registered_loaders.append(
    LoaderEntry(load_xml, "xml",
                (lambda source: "xml" in mimetypes.guess_type(source)[0])))


def load_dbm(source, absolute_resolved_path, **options):
    return dbm.open(absolute_resolved_path, "r")


registered_loaders.append(LoaderEntry(load_dbm, "dbm", None))


@contextlib.contextmanager
def load_import_module(source, **options):
    yield importlib.import_module(source)


registered_loaders.append(
    LoaderEntry(load_import_module, "import-module", None))
