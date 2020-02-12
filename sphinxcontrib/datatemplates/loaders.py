import contextlib
import csv
import dbm
import defusedxml.ElementTree as ET
import importlib
import json
import mimetypes
import pathlib
import yaml
from typing import Sequence, Mapping, Union, Any

registered_loaders = []


class LoaderEntry:
    def __init__(self, loader, name, match_source):
        self.loader = loader
        self.name = name
        self.match_source = match_source


def loader_for_source(source, default=None):
    "Return the loader for the named source."
    for e in registered_loaders:
        if e.match_source is not None and e.match_source(source):
            return e.loader
    return default


def loader_by_name(name, default=None):
    "Return the loader registered with the given name."
    for e in registered_loaders:
        if e.name == name:
            return e.loader
    return default


def mimetype_loader(name, mimetype):
    "A data loader for the exact mimetype."

    def check_mimetype(source):
        guess = mimetypes.guess_type(source)[0]
        if not guess:
            return False
        return guess == mimetype

    return data_source_loader(name, check_mimetype)


def lenient_mimetype_loader(name, mimetype_fragment):
    "A data loader for a mimetype containing the given substring."

    def check_mimetype(source):
        guess = mimetypes.guess_type(source)[0]
        if not guess:
            return False
        return mimetype_fragment in guess

    return data_source_loader(name, check_mimetype)


def file_extension_loader(name, extensions):
    "A data loader for filenames ending with one of the given extensions."

    def check_ext(filename):
        return pathlib.Path(filename).suffix.lower() in set(
            e.lower() for e in extensions)

    return data_source_loader(name, check_ext)


def data_source_loader(name, match_source=None):
    """Add a named loader

    Add a named data loader with an optional function for matching to
    source names.

    """

    def wrap(loader_func):
        registered_loaders.append(LoaderEntry(loader_func, name, match_source))
        return loader_func

    return wrap


class LoaderBase(contextlib.AbstractContextManager):
    def __init__(self, source: Any, **options):
        self.source = source
        self.options = options

    def __enter__(self) -> Mapping:
        return NotImplemented

    def __exit__(self, exc_type, exc_value, traceback):
        return super().__exit__(exc_type, exc_value, traceback)


class ChainLoaderBase(LoaderBase):
    chain: Sequence[LoaderBase] = ()

    def __enter__(self):
        es = contextlib.ExitStack().__enter__()
        options = self.options
        source = self.source
        for loader in self.chain:
            source = es.enter_context(loader(source, **options))
        self.es = es
        return source

    def __exit__(self, exc_type, exc_value, traceback):
        return self.es.__exit__(exc_type, exc_value, traceback)


class FilesystemStringLoader(LoaderBase):
    def __init__(self,
                 source: Union[str, pathlib.PurePath],
                 encoding="utf-8-sig",
                 **options):
        super().__init__(source, **options)
        self.encoding = encoding

    def __enter__(self):
        with open(self.source, "rt", encoding=self.encoding) as f:
            return f.read()


class FilesystemBytesLoader(LoaderBase):
    def __init__(self, source: Union[str, pathlib.PurePath], **options):
        super().__init__(source, **options)

    def __enter__(self):
        with open(self.source, "rb") as f:
            return f.read()


@data_source_loader("nodata")
class NoDataLoader(LoaderBase):
    def __enter__(self):
        return None


@data_source_loader("literal-json")
class LiteralJSONLoader(LoaderBase):
    def __init__(self, source: Union[str, bytes, bytearray], **options):
        super().__init__(source, **options)

    def __enter__(self):
        return json.loads(self.source)


@mimetype_loader("json", "application/json")
class JSONLoader(ChainLoaderBase):
    chain = (FilesystemBytesLoader, LiteralJSONLoader)


@data_source_loader("literal-yaml")
class LiteralYAMLLoader(LoaderBase):
    def __init__(self,
                 source: Union[str, bytes, bytearray],
                 multiple_documents=False,
                 **options):
        super().__init__(source, **options)
        self.multiple_documents = multiple_documents

    def __enter__(self):
        if self.multiple_documents:
            return tuple(yaml.safe_load_all(self.source))
        else:
            return yaml.safe_load(self.source)


@file_extension_loader("yaml", ['.yml', '.yaml'])
class YAMLLoader(ChainLoaderBase):
    chain = (FilesystemBytesLoader, LiteralYAMLLoader)


@data_source_loader("literal-csv")
class LiteralCSVLoader(LoaderBase):
    def __init__(self,
                 source: Union[str, bytes, bytearray],
                 headers=False,
                 dialect=None,
                 **options):
        super().__init__(source, **options)
        self.headers = headers
        self.dialect = dialect

    def __enter__(self):
        lines = self.source.splitlines(keepends=False)
        headers = self.headers
        dialect = self.dialect
        if self.dialect == "auto":
            sample = "\n".join(lines[:100])
            sniffer = csv.Sniffer()
            dialect = sniffer.sniff(sample)
        if headers:
            if dialect is None:
                r = csv.DictReader(lines)
            else:
                r = csv.DictReader(lines, dialect=dialect)
        else:
            if dialect is None:
                r = csv.reader(lines)
            else:
                r = csv.reader(lines, dialect=dialect)
        return tuple(r)


@file_extension_loader("csv", [".csv"])
class CSVLoader(ChainLoaderBase):
    chain = (FilesystemStringLoader, LiteralCSVLoader)


@data_source_loader("literal-xml")
class LiteralXMLLoader(LoaderBase):
    def __init__(self, source: Union[str, bytes, bytearray], **options):
        super().__init__(source, **options)

    def __enter__(self):
        return ET.fromstring(self.source)


@lenient_mimetype_loader('xml', 'xml')
class XMLLoader(ChainLoaderBase):
    chain = (FilesystemBytesLoader, LiteralXMLLoader)


@data_source_loader("import-module")
class ImportModuleLoader(LoaderBase):
    def __init__(self, source: str, **options):
        super().__init__(source, **options)

    def __enter__(self):
        return importlib.import_module(self.source)


@file_extension_loader("dbm", ['.dbm'])
def load_dbm(source, **options):
    return dbm.open(source, "r")
