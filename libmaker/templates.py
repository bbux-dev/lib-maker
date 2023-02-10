_GIT_IGNORE = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*,cover
.hypothesis/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# IPython Notebook
.ipynb_checkpoints

# pyenv
.python-version

# celery beat schedule file
celerybeat-schedule

# dotenv
.env

# virtualenv
.venv/
venv/
ENV/

# Spyder project settings
.spyderproject

# Rope project settings
.ropeproject

# intellij
.idea

# mypy
.mypy_cache"""

_PYPROJECT_TOML = """[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"
"""

_README = """{{ project }}
=============

TODO: Fill in README
"""

_SETUP_PY = """# -*- coding: utf-8 -*-
import setuptools

if __name__ == "__main__":
    setuptools.setup()
"""

_SETUP_CFG = """[metadata]
name = {{ project }}
version = {{ version | default('0.1.0', true) }}
description = {{ description }}
long_description = file: README.md
long_description_content_type = text/markdown; charset=UTF-8
url = {{ url | default('https://github.com/', true) }}
author = {{ author }}
author_email = {{ email }}
license = {{ license }}

[options]
packages = find:

install_requires =
{%- for requirement in requirements %}
    {{ requirement }}
{%- endfor %}

[options.packages.find]
exclude = tests

{%- if script %}
[options.entry_points]
console_scripts =
    {{ script }} = {{ package }}.__main__:main
{%- endif %}

{%- if package_data %}
[options.package_data]
{{ package_data }}
{%- endif %}

[options.extras_require]
test =
    pytest
    pycodestyle
    pytest-cov
all =
    %(test)s
"""

_PACKAGE_INIT = """\"\"\"Main module for {{ package }}\"\"\"
import logging

log = logging.getLogger(__name__)


def doit(input: str, output: str):
    \"\"\"Where the magic happens\"\"\"
    log.info("Working hard...")
"""

CORE = {
    ".gitignore": _GIT_IGNORE,
    "pyproject.toml": _PYPROJECT_TOML,
    "README.md": _README,
    "setup.cfg": _SETUP_CFG,
    "setup.py": _SETUP_PY,
    "{{ package }}/__init__.py": _PACKAGE_INIT,
    "{{ package }}/py.typed": "\n",
    "tests/__init__.py": "\n"
}
MAIN = """import argparse
import logging

import {{ package }}

log = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('-i', '--input', required=True,
                        help='where to get the input')

    parser.add_argument('-o', '--output', default=".",
                        help='where to put the output')

    levels = ('debug', 'info', 'warning', 'error', 'critical')
    parser.add_argument('-l', '--log-level', dest='level', default='info', choices=levels)

    args = parser.parse_args()
    _configure_logging(args.level.upper())
    # Do Stuff
    log.info("Doing stuff...")
    {{ package }}.doit(args.input, args.output)


def _configure_logging(log_level):
    logging.basicConfig(level=log_level,
                        format='%(levelname)s %(name)s %(message)s')


if __name__ == '__main__':
    main()
"""