from __future__ import print_function

import argparse
import jinja2

from . import standalone


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--templates-folder',
                        help='the path to the templates folder',
                        default="./templates")
    subparsers = parser.add_subparsers(title="subcommand", dest="cmd")
    for name, dt in standalone.datatemplate_names.items():
        p = subparsers.add_parser(name)
        for option_name in dt.option_spec.keys():
            p.add_argument("--" + option_name, default=argparse.SUPPRESS)
    args = parser.parse_args()
    options = vars(args).copy()
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(
        options.pop('templates_folder'), encoding='utf-8-sig'))

    datatemplate = standalone.datatemplate_names[options.pop("cmd")](env,
                                                                     options)
    print(datatemplate.run())


if __name__ == "__main__":
    main()