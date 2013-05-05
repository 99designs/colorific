# -*- coding: utf-8 -*-
#
#  setup.py
#  colorific
#

"""
Package information for colorific.
"""

import sys

# check for the supported Python version
version = tuple(sys.version_info[:2])
if version != (2, 7):
    sys.stderr.write(
        'colorific requires Python 2.7 (you have %d.%d)\n' % version)
    sys.stderr.flush()
    sys.exit(1)

import os.path
from setuptools import setup

PROJECT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__)))
README_FILE_PATH = os.path.join(PROJECT_DIR, 'README.rst')
REQUIREMENTS_FILE_PATH = os.path.join(PROJECT_DIR, 'requirements.pip')
VERSION = __import__('colorific').get_version()

setup(
    name='colorific',
    version=VERSION,
    description='Automatic color palette detection',
    long_description=file(README_FILE_PATH).read(),
    author='Lars Yencken',
    author_email='lars@yencken.org',
    url='http://github.com/99designs/colorific',
    py_modules=['colorific'],
    install_requires=[
        i.strip() for i in file(REQUIREMENTS_FILE_PATH).readlines()],
    license='ISC',
    entry_points={
        'console_scripts': [
            'colorific = colorific:main',
        ],
    },
)
