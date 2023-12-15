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
