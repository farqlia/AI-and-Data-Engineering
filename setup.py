#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import re

from setuptools import setup

# run pip install -e . to make this a package

# solution found in https://stackoverflow.com/a/39671214
# not the best, but it works
__version__ = re.search(
    r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',  # It excludes inline comment too
    io.open('ai_data_eng/__init__.py', encoding='utf_8_sig').read()
).group(1)

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as f:
    print(f.read().splitlines())

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as f:
    required = f.read().splitlines()

setup(
    name='ai-data-eng-prediction',
    version=__version__,
    packages=['ai_data_eng'],
    description='AI and Data Engineering.',
    author='Julia Farganus',
    author_email='juliafarganus@gmail.com',
    maintainer_email='juliafarganus@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3.10'
    ],
    # long_description=open(os.path.join(os.path.dirname(__file__), 'index.rst')).read(),
    install_requires=required,
)
