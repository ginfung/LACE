"""A setuptools based setup module for LACE"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from codecs import open
from os import path
from setuptools import setup, find_packages

import versioneer, sys

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as readme_file:
    readme = readme_file.read()

with open(path.join(here, 'HISTORY.rst'), encoding='utf-8') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'click',
    'numpy'
]

test_requirements = [
]

# The source dist comes with batteries included, the wheel can use pip to get the rest
is_wheel = 'bdist_wheel' in sys.argv

excluded = []
if is_wheel:
    excluded.append('extlibs.future')

def exclude_package(pkg):
    for exclude in excluded:
        if pkg.startswith(exclude):
            return True
    return False

def create_package_list(base_package):
    return ([base_package] +
            [base_package + '.' + pkg
             for pkg
             in find_packages(base_package)
             if not exclude_package(pkg)])


setup(
    name='lace',
    # version=versioneer.get_version(),
    # cmdclass=versioneer.get_cmdclass(),
    version = '1.0.1',

    description=" Lace-scale Assurance of Confidentiality Environment",
    long_description=readme + '\n\n' + history,
    author="Jianfeng Chen",
    author_email='jchen37@ncsu.edu',
    url='https://github.com/ginfung/LACE',
    
    # packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    packages = create_package_list('lace'),
    # entry_points={
    #     'console_scripts':[
    #         'LACE=lace.cli:cli',
    #         ],
    #     },
    # include_package_data=True,
    install_requires=requirements,
    license="MIT",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Database', 
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements,
)
