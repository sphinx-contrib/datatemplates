from __future__ import annotations
import pytest

from pathlib import Path
from typing import TYPE_CHECKING

from bs4 import BeautifulSoup

if TYPE_CHECKING:
    from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx("html", testroot="custom-template-bridge")
def test_custom_template_bridge(app: SphinxTestApp):
    app.builder.build_all()

    assert app._warncount == 0, "\n".join(app.messagelog)

    result = Path(app.outdir, "index.html").read_text()
    soup = BeautifulSoup(result, "html.parser")
    tag = soup.select("div.body > p")[0]

    assert tag.text == "SOME_VALUE"
