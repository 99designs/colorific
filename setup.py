# -*- coding: utf-8 -*-
#
#  setup.py
#  colorific
#

"""
Package information for colorific.
"""

import os
from setuptools import setup

readme = os.path.join(os.path.dirname(__file__), 'README.md')

setup(
    name='colorific',
    version='0.2.0',
    description='Automatic color palette detection',
    long_description=open(readme).read(),
    author='Lars Yencken',
    author_email='lars@yencken.org',
    url='http://github.com/99designs/colorific',
    py_modules=['colorific'],
    install_requires=[
            'PIL>=1.1.6',
            'colormath>=1.0.8',
            'numpy>=1.6.1',
        ],
    license='ISC',
    entry_points={
        'console_scripts': [
                'colorific = colorific:main',
            ],
        },
)
