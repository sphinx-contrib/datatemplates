from __future__ import annotations

from typing import TYPE_CHECKING

from sphinx.jinja2glue import BuiltinTemplateLoader

if TYPE_CHECKING:
    from typing import List, Optional

    from sphinx.builders import Builder
    from sphinx.theming import Theme


def upperstring(input: str):
    """Custom filter"""
    return input.upper()


class CustomTemplateLoader(BuiltinTemplateLoader):
    def init(
        self,
        builder: Builder,
        theme: Optional[Theme] = None,
        dirs: Optional[List[str]] = None,
    ) -> None:
        super().init(builder, theme, dirs)
        self.environment.filters["upperstring"] = upperstring
