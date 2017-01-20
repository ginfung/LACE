"""A setuptools based setup module for LACE"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from distutils.core import setup
from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as readme_file:
    readme = readme_file.read()
with open(path.join(here, 'HISTORY.rst'), encoding='utf-8') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'click',
    'numpy'
]

test_requirements = []

setup(
    name = 'lace',
    version = '2.1.2',

    author = 'Jianfeng Chen',
    author_email = 'jchen37@ncsu.edu',
    url = 'https://github.com/ginfung/lace',

    description = 'Lace-scale Assurance of Confidentiality Environment Framework',
    long_description=readme + '\n\n' + history,

    packages = ['lace'],
    include_package_data = True,

    license= 'MIT',

    install_requires = requirements,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Database', 
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
    ],
	test_suite = "tests",
	tests_require=test_requirements,
)
