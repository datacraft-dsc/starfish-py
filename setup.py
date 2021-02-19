#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import os
from os.path import join

from setuptools import (
    setup,
    find_packages
)

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.md') as changelog_file:
    changelog = changelog_file.read()


install_requirements = [
    'web3',
    'typing_extensions',
    'mongoquery',
    'convex-api-py == 0.1.*',
]

setup_requirements = ['pytest-runner', ]

test_requirements = [
    'flake8',
    'pytest',
    'isort',
    'mypy',
    'pyyaml',
]

# Possibly required by developers of starfish-py:
dev_requirements = [
    'bumpversion',
    'isort',
    'mypy',
]

docs_requirements = [
    'Sphinx',
    'sphinx-rtd-theme',
    'sphinxcontrib-apidoc',
    'sphinxcontrib-plantuml',
    'sphinx-automodapi',
    'pygments',
]

setup(
    author="Datacraft",
    author_email='devops@datacraft.sg',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    description="Developer Toolkit for Decentralised Data Ecosystems",
    extras_require={
        'test': test_requirements,
        'docs': docs_requirements,
        'dev': dev_requirements + test_requirements + docs_requirements,
    },
    install_requires=install_requirements,
    #dependency_links=dependency_links,
    license="Apache Software License 2.0",
    long_description=readme,
    long_description_content_type='text/markdown',
    keywords='starfish-py',
    name='starfish-py',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'starfish.contract': ['data/*.json.gz', 'data/*.json']
    },
    scripts=[
        'tools/starfish_tools',
    ],
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/datacraft-dsc/starfish-py',
    version='0.16.8',
    zip_safe=False,
)
