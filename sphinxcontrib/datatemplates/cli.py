from __future__ import print_function

import argparse
import json

import jinja2
import yaml

from sphinxcontrib.datatemplates import helpers


def _load_data(filename):
    if filename.endswith('.yaml'):
        with open(filename, 'r') as f:
            return yaml.load(f)
    elif filename.endswith('.json'):
        with open(filename, 'r') as f:
            return json.load(f)
    else:
        raise NotImplementedError('cannot load file type of %s' %
                                  filename)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'source',
        help='the path to the data file',
    )
    parser.add_argument(
        'template',
        help='the path to the template file',
    )
    args = parser.parse_args()

    data = _load_data(args.source)

    with open(args.template, 'r') as f:
        template_body = f.read().decode('utf-8')

    template = jinja2.Template(template_body)
    rendered = template.render(
        make_list_table=helpers.make_list_table,
        make_list_table_from_mappings=helpers.make_list_table_from_mappings,
        data=data,
    )
    print(rendered)
