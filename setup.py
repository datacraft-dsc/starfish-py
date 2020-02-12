#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup
import os
from os.path import join

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.md') as changelog_file:
    changelog = changelog_file.read()

install_requirements = [
    'squid-py==0.7.1',
    'ocean-events-handler==0.1.2',
    'ocean-utils==0.1.0',
    'ocean-keeper==0.1.1',
    'ocean-secret-store-client==0.0.1',
    'requests==2.21.0',
    'plecos',
    'coloredlogs',
    'eciespy',
    'pyopenssl',
    'pycryptodome',
    'PyJWT',  # not jwt
    'PyYAML==4.2b4',
    'web3==4.5.0',
]

setup_requirements = ['pytest-runner', ]

test_requirements = [
    'codacy-coverage',
    'coverage',
    'docker',
    'flake8',
    'mccabe',
    'pyflakes',
    'pytest',
    'tox',
]

# Possibly required by developers of starfish-py:
dev_requirements = [
    'bumpversion',
    'pkginfo',
    'twine',
    'watchdog',
]

docs_requirements = [
    'Sphinx',
    'sphinx-rtd-theme',
    'sphinxcontrib-apidoc',
    'sphinxcontrib-plantuml',
    'sphinx-automodapi',
    'pygments',
]

packages = []
for d, _, _ in os.walk('starfish'):
    if os.path.exists(join(d, '__init__.py')):
        packages.append(d.replace(os.path.sep, '.'))

setup(
    author="dex-company",
    author_email='devops@dex.sg',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    description="Ocean/squid-py wrapper.",
    extras_require={
        'test': test_requirements,
        'dev': dev_requirements + test_requirements + docs_requirements,
    },
    install_requires=install_requirements,
    license="Apache Software License 2.0",
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='starfish-py',
    name='starfish-py',
    packages=packages,
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/DEX-Company/starfish-py',
    version='0.6.4',
    zip_safe=False,
)
