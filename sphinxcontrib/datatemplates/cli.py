from __future__ import print_function

import argparse
import jinja2

from . import standalone


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--templates-folder',
                        help='path to the templates folder',
                        default='./templates')

    # Add subcommand for each datatemplate
    subparsers = parser.add_subparsers(title="subcommand", dest="cmd")
    for name, dt in standalone.datatemplate_names.items():
        p = subparsers.add_parser(name)
        for option_name in dt.option_spec.keys():
            p.add_argument("--" + option_name, default=argparse.SUPPRESS)

    args = parser.parse_args()

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(
        args.templates_folder, encoding='utf-8-sig'))

    # create options dict for datatemplate
    options = vars(args).copy()
    del options['templates_folder']
    del options['cmd']

    # do the actual work
    datatemplate = standalone.datatemplate_names[args.cmd](env, options)
    print(datatemplate.run())


if __name__ == "__main__":
    main()
