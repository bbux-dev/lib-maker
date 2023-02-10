lib-maker
=============

Tool for creating skeleton for a new python projects.

Creates the following structure:

```
/:
 .gitignore
 README.md
 pyproject.toml
 requirements.txt
 setup.cfg
 setup.py
 libmaker/:
   __init__.py
   __main__.py # <- optional when --script supplied
 tests/:
   __init__.py
```

# Installation

```shell
pip install git+https://github.com/bbux-dev/lib-maker.git
```
# Usage Example

The example below will crete a project zebra-corn one directory up with a
script called dazzle.  After creating the project you are able to pip install it
and get a basic cli tool:

```shell
mklib zebra-corn --package zebracorn -s dazzle \
  --author "Brian Buxton" \
  --email "bbux-dev@gmail.com" \
  -d "Example project generated with lib-maker" \
  --outdir ../ \
  -r requests pandas \
  --overwrite

cd ../zebra-corn

pip install .

dazzle -h
usage: dazzle [-h] -i INPUT [-o OUTPUT]
              [-l {dubug,info,warning,error,critical}]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        where to get the input
  -o OUTPUT, --output OUTPUT
                        where to put the output
  -l {dubug,info,warning,error,critical}, --log-level {dubug,info,warning,error,critical}
```

# Custom Package Directory

Some projects prefer to have the code in a root folder other than the package name (e.g. src/). You can use the
`--package-dir <name>` flag to specify this.  Example:

```shell
mklib llama-corn --package llamacorn -s spitter \
  --author "Brian Buxton" \
  --email "bbux-dev@gmal.com" \
  -d "Example project generated with lib-maker" \
  --outdir . \
  -r requests pandas \
  --overwrite \
  --package-dir src
```

This will create this directory structure:

```
llama-corn/:
  .gitignore
  README.md
  pyproject.toml
  requirements.txt
  setup.cfg
  setup.py
  src/llamacorn/:
    __init__.py
    __main__.py
  tests/:
    __init__.py
```

Note: If using pytest for tests you may need to run them in a slightly different way when using this structure. See:
https://docs.pytest.org/en/7.1.x/explanation/goodpractices.html#tests-outside-application-code
https://docs.pytest.org/en/7.1.x/explanation/pythonpath.html#pytest-vs-python-m-pytest

For the example above:

```shell
pip install --editable .
python -m pytest -v -s --cov=src/llamacorn
```