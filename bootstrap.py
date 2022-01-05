import os
import argparse
import json
import logging

from jinja2 import Environment, BaseLoader, select_autoescape

# import libmaker
from templates import CORE, MAIN

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

    makeit(args.outdir, args.project, args.overwrite, **config)


def _add_arg_override_to_config(config, key, value, default=None):
    """ adds the value to config if defined """
    if value:
        config[key] = value
    elif default:
        config[key] = default


def makeit(outdir: str, name: str, overwrite: bool = False, **kwargs):
    """
    Makes the project from the given configuration

    Args:
        outdir: where to create to project
        name: name of the project
        overwrite: if existing files and directories should be overwritten

    Keyword Args:
        author: for project
        description: of project
        email: author email
        license: type of license
        project: name of project
        package: name of package
        package_data: package data to include if any
        requirements: list of required dependencies
        script: executable script name
        url: for project
        version: of project

    Returns:
        Path to generated project
    """
    print("making it...")
    root = os.path.join(outdir, name)
    if os.path.exists(root) and not overwrite:
        log.warning('Directory %s already exists and --overwrite not specified')
        return
    if not os.path.exists(root):
        os.makedirs(root)
    _make_structure(root, kwargs.get('package'))
    _make_core(root, kwargs)
    print("done making it, see: " + root)


def _make_structure(root: str, package: str):
    """Creates the project structure"""
    paths = [
        os.path.join(root, package),
        os.path.join(root, 'tests'),
    ]
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)


def _make_core(root, data):
    """Populate and write the template files to the given directory """
    env = Environment(
        loader=BaseLoader(),
        autoescape=select_autoescape(['html', 'xml'])
    )
    for path_template, template_str in CORE.items():
        path_str = _render(env, path_template, data)
        path = os.path.join(root, path_str)
        data_str = _render(env, template_str, data)
        with open(path, 'w') as handle:
            handle.write(data_str)
    if 'script' in data:
        package = data.get('package')
        path = os.path.join(root, package, '__main__.py')
        data_str = _render(env, MAIN, data)
        with open(path, 'w') as handle:
            handle.write(data_str)


def _render(env, template_str, data):
    """Uses the environment to render the provided template string using the provided data"""
    template = env.from_string(template_str)
    return template.render(data)


if __name__ == '__main__':
    main()
