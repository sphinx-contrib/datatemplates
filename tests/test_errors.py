from __future__ import annotations

from typing import TYPE_CHECKING
import pytest

if TYPE_CHECKING:
    from io import StringIO
    from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx("html", testroot="empty-source")
def test_empty_source(app: SphinxTestApp, warning: StringIO):
    app.builder.build_all()
    expected_error_str = (
        f"{app.srcdir / 'index.rst'}:1: ERROR: Source file is required"
    )
    assert expected_error_str in warning.getvalue()


@pytest.mark.sphinx("html", testroot="nonexistent-source")
def test_nonexisting_source(app: SphinxTestApp, warning: StringIO):
    app.builder.build_all()
    expected_error_str = (
        f"{app.srcdir / 'index.rst'}:1: "
        "ERROR: Source file 'sample1.json' not found"
    )
    assert expected_error_str in warning.getvalue()


@pytest.mark.sphinx("html", testroot="empty-template")
def test_empty_template(app: SphinxTestApp, warning: StringIO):
    app.builder.build_all()
    expected_error_str = (
        f"{app.srcdir / 'index.rst'}:1: ERROR: Template is empty"
    )
    assert expected_error_str in warning.getvalue()


@pytest.mark.sphinx("html", testroot="nonexistent-template")
def test_nonexistent_template(app: SphinxTestApp, warning: StringIO):
    app.builder.build_all()
    expected_error_str = (
        f"{app.srcdir / 'index.rst'}:1: "
        "ERROR: Template file 'sample1.tmpl' not found"
    )
    assert expected_error_str in warning.getvalue()


@pytest.mark.sphinx("html", testroot="nonexistent-template-filter")
def test_nonexistent_template_filter(app: SphinxTestApp, warning: StringIO):
    app.builder.build_all()
    expected_error_str = (
        f"{app.srcdir / 'index.rst'}:1: "
        "ERROR: Error in template file 'sample.tmpl' line 1: "
        "No filter named 'some_filter'."
    )
    assert expected_error_str in warning.getvalue()


@pytest.mark.sphinx("html", testroot="incorrect-template-syntax")
def test_incorrect_template_syntax(app: SphinxTestApp, warning: StringIO):
    app.builder.build_all()
    expected_error_str = (
        f"{app.srcdir / 'index.rst'}:1: "
        "ERROR: Error in template file 'sample.tmpl' line 1: "
        "unexpected '}'"
    )
    assert expected_error_str in warning.getvalue()


@pytest.mark.sphinx("html", testroot="incorrect-json-syntax")
def test_incorrect_json_syntax(app: SphinxTestApp, warning: StringIO):
    app.builder.build_all()
    expected_error_str = (
        f"{app.srcdir / 'index.rst'}:1: "
        "ERROR: Error in source 'sample.json': "
        "Invalid control character at: line 2 column 28 (char 29)"
    )
    assert expected_error_str in warning.getvalue()


@pytest.mark.sphinx("html", testroot="incorrect-yaml-syntax")
def test_incorrect_yaml_syntax(app: SphinxTestApp, warning: StringIO):
    app.builder.build_all()
    expected_error_str = (
        f"{app.srcdir / 'index.rst'}:1: "
        "ERROR: Error in source 'sample.yaml': "
        "while parsing a block collection\n"
        '  in "sample.yaml", line 11, column 3\n'
        "expected <block end>, but found '?'\n"
        '  in "sample.yaml", line 12, column 3'
    )
    assert expected_error_str in warning.getvalue()


@pytest.mark.sphinx("html", testroot="incorrect-xml-syntax")
def test_incorrect_xml_syntax(app: SphinxTestApp, warning: StringIO):
    app.builder.build_all()
    expected_error_str = (
        f"{app.srcdir / 'index.rst'}:1: "
        "ERROR: Error in source 'sample.xml': "
        "not well-formed (invalid token): line 2, column 4"
    )
    assert expected_error_str in warning.getvalue()


@pytest.mark.sphinx("html", testroot="incorrect-import-module")
def test_incorrect_import_module(app: SphinxTestApp, warning: StringIO):
    app.builder.build_all()
    expected_error_str = (
        f"{app.srcdir / 'index.rst'}:1: "
        "ERROR: Error in source 'some_module': No module named 'some_module'"
    )
    assert expected_error_str in warning.getvalue()


@pytest.mark.sphinx("html", testroot="incorrect-dbm")
def test_incorrect_dbm(app: SphinxTestApp, warning: StringIO):
    app.builder.build_all()
    expected_error_str = (
        f"{app.srcdir / 'index.rst'}:1: "
        "ERROR: Error in source 'sampledbm': "
        "db type could not be determined"
    )
    assert expected_error_str in warning.getvalue()
