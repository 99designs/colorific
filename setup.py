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
    sys.stderr.write('colorific requires Python 2.7 (you have %d.%d)\n' %
            version)
    sys.stderr.flush()
    sys.exit(1)

import os
from setuptools import setup

readme = os.path.join(os.path.dirname(__file__), 'README.md')

setup(
    name='colorific',
    version='0.2.1',
    description='Automatic color palette detection',
    long_description=open(readme).read(),
    author='Lars Yencken',
    author_email='lars@yencken.org',
    url='http://github.com/99designs/colorific',
    py_modules=['colorific'],
    install_requires=[
            'Pillow==1.7.8',
            'colormath>=1.0.8',
            'numpy>=1.6.1',
        ],
    dependency_links=[
            'http://github.com/python-imaging/Pillow/tarball/master#egg=Pillow-1.7.8',
        ],
    license='ISC',
    entry_points={
        'console_scripts': [
                'colorific = colorific:main',
            ],
        },
)
