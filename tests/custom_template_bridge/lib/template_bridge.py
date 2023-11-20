from sphinx.builders import Builder
from sphinx.jinja2glue import BuiltinTemplateLoader
from sphinx.theming import Theme


def upperstring(input: str):
    """Custom filter"""
    return input.upper()


class CustomTemplateLoader(BuiltinTemplateLoader):
    def init(
        self,
        builder: Builder,
        theme: Theme | None = None,
        dirs: list[str] | None = None,
    ) -> None:
        super().init(builder, theme, dirs)
        self.environment.filters["upperstring"] = upperstring
