# -*- coding: utf-8 -*-
#
#  setup.py
#  colorific
#

"""
Package information for colorific.
"""

import os.path

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

PROJECT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__)))
README_PATH = os.path.join(PROJECT_DIR, 'README.rst')
REQUIREMENTS_PATH = os.path.join(PROJECT_DIR, 'requirements.pip')
VERSION = __import__('colorific').get_version()

setup(
    name='colorific',
    version=VERSION,
    description='Automatic color palette detection',
    long_description=open(README_PATH).read(),
    author='Lars Yencken',
    author_email='lars@yencken.org',
    url='http://github.com/99designs/colorific',
    license='ISC',
    packages=['colorific'],
    zip_safe=False,
    install_requires=[
        'Pillow>=2.6.1',
        'colormath>=2.0.2',
        'numpy>=1.9.0',
    ],
    entry_points={'console_scripts': ['colorific = colorific.script:main']},
    test_suite='tests',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
