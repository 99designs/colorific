# -*- coding: utf-8 -*-
#
#  setup.py
#  palette_detect
#

"""
Package information for palette_detect.
"""

import os
from setuptools import setup

readme = os.path.join(os.path.dirname(__file__), 'README.rst')

setup(
    name='palette_detect',
    version='0.1.0',
    description='Palette detection from images.',
    long_description=open(readme).read(),
    author='Lars Yencken',
    author_email='lars@yencken.org',
    url='http://bitbucket.org/larsyencken/palette-detect',
    scripts=['palette_detect'],
    install_requires=[
            'PIL>=1.1.6',
            'colormath>=1.0.8',
            'numpy>=1.6.1',
        ],
    license='ISC',
)
