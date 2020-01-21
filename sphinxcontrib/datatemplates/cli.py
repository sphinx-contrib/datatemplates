from __future__ import print_function

import argparse
import io
import os.path

import jinja2

from sphinxcontrib.datatemplates import helpers
from sphinxcontrib.datatemplates import loaders


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--config-file',
        help='the path to conf.py',
    )
    parser.add_argument(
        '--option',
        '-o',
        action='append',
        help='options given as key:value passed through to loader and template'
    )
    parser.add_argument(
        'template',
        help='the path to the template file',
    )
    parser.add_argument(
        'source',
        help='the path to the data file',
    )

    args = parser.parse_args()

    config_globals = {}
    if args.config_file:
        with io.open(args.config_file, 'r', encoding='utf-8-sig') as f:
            config_body = f.read()
        exec(config_body, config_globals)
    config_globals.update(
        {
            k.replace("-", "_"): v
            for k, _, v in (s.partition(':') for s in args.option)
        }, **{
            "source": args.source,
            "template": args.template,
            "absolute_resolved_path": os.path.abspath(args.source)
        })

    load = loaders.loader_for_source(args.source)

    with io.open(args.template, 'r', encoding='utf-8-sig') as f:
        template_body = f.read()

    template = jinja2.Template(template_body)
    with load(**config_globals) as data:
        rendered = template.render(
            make_list_table=helpers.make_list_table,
            make_list_table_from_mappings=helpers.
            make_list_table_from_mappings,
            data=data,
            **config_globals,
        )
    print(rendered)


if __name__ == '__main__':
    main()
