import contextlib
import json
import yaml
import defusedxml.ElementTree as ET
import dbm
import importlib
import csv


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


@contextlib.contextmanager
def load_json(source, absolute_resolved_path, encoding='utf-8-sig', **options):
    with open(absolute_resolved_path, 'r', encoding=encoding) as f:
        yield json.load(f)


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


@contextlib.contextmanager
def load_xml(source, absolute_resolved_path, **options):
    yield ET.parse(absolute_resolved_path).getroot()


def load_dbm(source, absolute_resolved_path, **options):
    return dbm.open(absolute_resolved_path, "r")


@contextlib.contextmanager
def load_import_module(source, **options):
    yield importlib.import_module(source)
