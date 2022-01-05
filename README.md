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
  --email "bbux-dev@gmal.com" \
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
