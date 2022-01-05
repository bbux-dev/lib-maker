import argparse
import json
import logging

import libmaker

log = logging.getLogger(__name__)
logging.basicConfig()


def main():
    """Main function for libmaker"""
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('project', help='Name of project')
    parser.add_argument('-c', '--config', help='Path to config file with populated configurations')
    parser.add_argument('-o', '--outdir', default='.', help='Path to write project to')
    parser.add_argument('-a', '--author', help='Project author')
    parser.add_argument('-d', '--description', help='Project description')
    parser.add_argument('-e', '--email', help='Project author email')
    parser.add_argument('-l', '--license', default="MIT", help='Project license')
    parser.add_argument('--package', help='Name of package if different from project')
    parser.add_argument('--package-data', help='Package data to include if any: i.e. * = *.json, '
                                               'would include all json files in package')
    parser.add_argument('-r', '--requirements', nargs='+',
                        help='One or more dependencies needed for package')
    parser.add_argument('-s', '--script', default="",
                        help='Name of executable, default is no executable')
    parser.add_argument('-u', '--url', help='Project url')
    parser.add_argument('-v', '--version', default="0.1.0",
                        help='Project version')
    parser.add_argument('--debug-config', dest='debug_config', action='store_true',
                        help='Print populated config to stdout')
    parser.add_argument('--overwrite', action='store_true',
                        help='Overwrite existing files and directories')

    args = parser.parse_args()

    config = {}
    if args.config:
        with open(args.config, 'r') as handle:
            config = json.load(handle)

    _add_arg_override_to_config(config, 'author', args.author)
    _add_arg_override_to_config(config, 'description', args.description)
    _add_arg_override_to_config(config, 'email', args.email)
    _add_arg_override_to_config(config, 'license', args.license)
    _add_arg_override_to_config(config, 'project', args.project)
    _add_arg_override_to_config(config, 'package', args.package, args.project)
    _add_arg_override_to_config(config, 'package_data ', args.package_data)
    _add_arg_override_to_config(config, 'requirements', args.requirements)
    _add_arg_override_to_config(config, 'script', args.script)
    _add_arg_override_to_config(config, 'url', args.url)
    _add_arg_override_to_config(config, 'version', args.version)

    if args.debug_config:
        print(json.dumps(config, indent=2))
        return

    libmaker.makeit(args.outdir, args.project, args.overwrite, **config)


def _add_arg_override_to_config(config, key, value, default=None):
    """ adds the value to config if defined """
    if value:
        config[key] = value
    elif default:
        config[key] = default


if __name__ == '__main__':
    main()
