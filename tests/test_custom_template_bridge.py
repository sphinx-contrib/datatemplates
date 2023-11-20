from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from bs4 import BeautifulSoup
from sphinx.testing.util import SphinxTestApp

if TYPE_CHECKING:
    from typing import Callable


def test_custom_template_bridge(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
):
    dataset_path = Path(os.path.dirname(__file__), "custom_template_bridge")
    shutil.copytree(dataset_path, tmp_path, dirs_exist_ok=True)

    app = make_app(srcdir=tmp_path, warning=sys.stdout)
    app.build()

    assert app._warncount == 0, "\n".join(app.messagelog)

    result = Path(app.outdir, "index.html").read_text()
    soup = BeautifulSoup(result, "html.parser")
    tag = soup.select("div.body > p")[0]

    assert tag.text == "SOME_VALUE"
