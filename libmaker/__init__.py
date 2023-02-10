"""Main module for libmaker"""
import logging
import os

from jinja2 import Environment, BaseLoader, select_autoescape

from .templates import CORE, MAIN

log = logging.getLogger(__name__)


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
        package_dir: directory to put package files in
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
    _make_structure(root, kwargs.get('package_dir'), kwargs.get('package'))
    _make_core(root, kwargs)
    print("done making it, see: " + root)


def _make_structure(root: str, package_dir: str, package: str):
    """Creates the project structure"""
    paths = [
        os.path.join(root, 'tests'),
    ]
    if package_dir is None:
        paths.append(os.path.join(root, package))
    else:
        paths.append(os.path.join(root, package_dir, package))
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
        package_dir = data.get('package_dir')
        if package_dir is None:
            path = os.path.join(root, package, '__main__.py')
        else:
            path = os.path.join(root, package_dir, package, '__main__.py')
        data_str = _render(env, MAIN, data)
        with open(path, 'w') as handle:
            handle.write(data_str)


def _render(env, template_str, data):
    """Uses the environment to render the provided template string using the provided data"""
    template = env.from_string(template_str)
    return template.render(data)
