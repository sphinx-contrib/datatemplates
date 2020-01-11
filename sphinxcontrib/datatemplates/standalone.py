from __future__ import print_function
from . import mixins
import argparse
import re

import jinja2


def _unrst(s):
    return re.sub(":\\S+?`(.+?)`", (lambda m: m.group(1)),
                  s.replace("``", '"'))


class DataTemplateStandalone:
    """
    Mixin for AbstractDataTemplateBase
    """

    def __init__(self, env, source, template, **options):
        self.env = env
        os = self.option_spec
        self.source = source
        self.options = {
            k: os[k](v) if k in os else v
            for k, v in options.items()
        }

    def run(self):
        resolved_path = self.source
        template_name = self.template
        template = self.env.get_template(template_name)

        with self._load_data_cm(resolved_path) as data:
            context = self._make_context(data)
            rendered_template = template.render(context)

        return rendered_template

    @classmethod
    def configure_parser(cls, parser, unrst=True):
        if unrst:
            parser.description = _unrst(cls.__doc__)
        else:
            parser.description = cls.__doc__
        parser.add_argument("source")
        parser.add_argument("template")
        parser.argument_default = argparse.SUPPRESS


class DataTemplateJSONStandalone(mixins.DataTemplateJSON,
                                 DataTemplateStandalone):
    """
    Load file at :py:attr:`source` via
    :py:func:`json.load` and render using :py:attr:`template`
    """

    @classmethod
    def configure_parser(cls, parser, unrst=True):
        super().configure_parser(parser, unrst)
        parser.add_argument(
            "--encoding",
            help=
            'The text encoding that will be used to read the source file. Defaults to "utf-8-sig".'
        )


class DataTemplateCSVStandalone(mixins.DataTemplateCSV,
                                DataTemplateStandalone):
    """
    Load file at :py:attr:`source` via
    :py:func:`csv.reader` or :py:class:`csv.DictReader` 
    depending on ``header`` and render using :py:attr:`template`.
    """

    @classmethod
    def configure_parser(cls, parser, unrst=True):
        super().configure_parser(parser, unrst)
        parser.add_argument(
            "--encoding",
            help=
            'The text encoding that will be used to read the source file. Defaults to "utf-8-sig".'
        )
        parser.add_argument(
            "--header",
            action='store_const',
            const=None,
            help=
            "Set to use csv.DictReader for reading the file. If not set csv.reader is used."
        )
        parser.add_argument(
            "--dialect",
            help=
            'Set to select a specific csv.Dialect. Set to "auto", to try autodetection. If not set the default dialect is used.'
        )


class DataTemplateYAMLStandalone(mixins.DataTemplateYAML,
                                 DataTemplateStandalone):
    """
    Load file at :py:attr:`source` via 
    PyYAML (:py:func:`yaml.safe_load`) and render using :py:attr:`template`.
    """

    @classmethod
    def configure_parser(cls, parser, unrst=True):
        super().configure_parser(parser, unrst)
        parser.add_argument(
            "--encoding",
            help=
            'The text encoding that will be used to read the source file. Defaults to "utf-8-sig".'
        )
        parser.add_argument(
            "--multiple-documents",
            action='store_const',
            const=None,
            help="Set to read multiple documents from the file into a list.")


class DataTemplateXMLStandalone(mixins.DataTemplateXML,
                                DataTemplateStandalone):
    """
    Load file at :py:attr:`source` via
    :py:func:`xml.etree.ElementTree.parse` (actually using ``defusedxml``) and render using :py:attr:`template`.
    """


class DataTemplateDBMStandalone(mixins.DataTemplateDBM,
                                DataTemplateStandalone):
    """
    Load DB at :py:attr:`source` via
    :py:func:`dbm.open` and render using :py:attr:`template`.
    """


class DataTemplateImportModuleStandalone(mixins.DataTemplateImportModule,
                                         DataTemplateStandalone):
    """
    Load module :py:attr:`source` (must be importable)  via 
    :py:func:`importlib.import_module` and render using :py:attr:`template`.
    """


datatemplate_names = {
    "json": DataTemplateJSONStandalone,
    "csv": DataTemplateCSVStandalone,
    "yaml": DataTemplateYAMLStandalone,
    "xml": DataTemplateXMLStandalone,
    "dbm": DataTemplateDBMStandalone,
    "import-module": DataTemplateImportModuleStandalone,
}


def argument_parser(unrst=True):
    parser = argparse.ArgumentParser()

    # Add subcommand for each datatemplate
    subparsers = parser.add_subparsers(title="subcommand", dest="cmd")
    for name, dt in datatemplate_names.items():
        p = subparsers.add_parser(name)
        dt.configure_parser(p, unrst=unrst)
        p.add_argument('--templates-folder',
                       help='Path to the templates folder. Defaults to "."',
                       default='.')
    return parser


def doc_argument_parser():
    return argument_parser(unrst=False)


def main():
    parser = argument_parser()

    args = parser.parse_args()

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(
        args.templates_folder, encoding='utf-8-sig'))

    # create options dict for datatemplate
    options = vars(args)

    # do the actual work
    datatemplate = datatemplate_names[args.cmd](env, args.source,
                                                args.template, **options)
    print(datatemplate.run())


if __name__ == "__main__":
    main()
