#!/bin/bash -xe

python setup.py sdist
twine check dist/*$(python setup.py --version)*
