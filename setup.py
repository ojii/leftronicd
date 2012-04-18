#!/usr/bin/env python
# -*- coding: utf-8 -*-
from leftronicd import __version__
from setuptools import setup, find_packages


with open('requirements.txt') as fobj:
    INSTALL_REQUIRES = [line.strip() for line in fobj.readlines() if line.strip()]

try:
    import json
except ImportError:
    INSTALL_REQUIRES.append('simplejson')

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Topic :: Software Development',
]

setup(
    name='leftronicd',
    version=__version__,
    description='A twisted based daemon to send metrics to leftronic.com',
    author='Jonas Obrist',
    author_email='ojiidotch@gmail.com',
    url='https://github.com/ojii/leftronicd',
    packages=find_packages(),
    license='BSD',
    platforms=['OS Independent'],
    install_requires=INSTALL_REQUIRES,
    entry_points="""
    [console_scripts]
    leftronicd = leftronicd.main:cli
    """,
)
