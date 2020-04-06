# starfish-py

![](https://github.com/DEX-Company/starfish-py/workflows/testing/badge.svg)
[![GitHub contributors](https://img.shields.io/github/contributors/DEX-Company/starfish-py.svg)](https://github.com/DEX-Company/starfish-py/graphs/contributors)
[![Barge Version](https://img.shields.io/badge/barge-develop-blue.svg)](https://github.com/DEX-Company/barge)

---

## Table of Contents

  - [About](#about)
  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Quickstart](#quickstart)
  - [Environment variables](#environment-variables)
  - [Testing](#testing)
  - [New Version](#new-version)
  - [Mailing Lists](#mailing-list)
  - [Maintainers](#maintainers)
  - [License](#license)

---

## About

Starfish is an open-sourced developer toolkit for the data economy. Available in flavours of Java, Python, and Clojure, it allows developers, data scientists and enterprises to create, interact, integrate and manage a data supply line through standardised and simple-to-use APIs.

Based on an underlying data ecosystem standard, Starfish provides high-level APIs for common tasks within the data economy, for example, registering/publishing an asset, for subsequent use in a data supply line. In this case, an asset can be any data set, model or data service. The high-level API also allows developers to invoke operation on an asset, e.g. computing a predictive model or anonymising sensitive personal information, among other capabilities.

Starfish works with blockchain networks, such as Ocean Protocol, and common web services through agents, allowing unprecedented flexibility in asset discovery and data supply line management.

Starfish-py provides user access and tools to work with the Ocean Protocol Network, delegating certain functions via the python library squid-py.

While we strive to deliver code at a high quality, please note, that there exist parts of the library that still need thorough testing.
Contributions – whether it is in the form of new features, better documentation or tests – are welcome.

## Prerequisites

Python >= 3.6

## Development

1. Clone this repo

    ```bash
    clone https://github.com/DEX-Company/starfish-py.git
    cd starfish-py
    ```

1. Set up a virtual environment

    ```bash
    virtualenv venv
    source venv/bin/activate
    ```

1. Install package requirements for starfish

    ```bash
    make install
    ```

1. Run the unit tests, without any supporting software/libraries outside of starfish

    ```bash
    make test_unit
    ```

1. To run the full test using the current remote implementation of [barge](https://github.com/DEX-Company/barge).

    ```bash
    git clone https://github.com/DEX-Company/barge.git
    cd barge
    git checkout develop
    ./start_ocean.sh --no-brizo --no-surfer --no-koi --no-aquarius --no-dashboard --no-secret-store --local-spree-node
    ```

    Or to run barge locally, using the same method above but using a script instead.

    ```bash
    export BARGE_URL=http://localhost
    scripts/setup_for_local_barge.sh
    ```


1. Run the integration tests

    ```
    pytest tests/integration
    ```

1. Run the all tests

    ```bash
    make tests
    ```

## Documentation

1. Build Sphinx documentation

    To build the Syphinx auto documentation, you need to do the following:
    ```bash
    make docs
    ```

The [documentation](https://dex-company.github.io/starfish-py) for this repo.


## Testing

Automatic tests are setup via github actions.
Our test use pytest framework.
The testing uses a barge docker image and surfer server.
See [github actions for testing](https://github.com/DEX-Company/starfish-py/blob/master/.github/workflows/testing.yml)

## New Version

The `bumpversion.sh` script helps to bump the project version. You can execute the script using as first argument {major|minor|patch} to bump accordingly the version.

## Mailing Lists

  * [developer@dex.sg][starfish-qa] -- General questions regarding the usage of Starfish.

## Git Development Cycle

Notes on the current development/release lifecyle.

### Start a new release
+   Get the latest develop branch `git checkout develop`
+   Bump to the next version `./bumpnersion.sh [patch|minor|major]`
+   Add version line in CHANGELOG.md

### Develop changes
+   Create branches for new PR's.. `git checkout -b new-branch`
+   Develop new feature/patch
+   Update CHANGELOG.md with changes made
+   Merge PR to develop.
+   Repeat until version completed

### Release the current version
+   Checkout master.    `git checkout master`
+   Merge master with develop.      `git merge develop`
+   Create release using web page

## Maintainers

 [Developer Dex team][developer@dex.sg]


## License

```
Copyright 2018 Ocean Protocol Foundation Ltd.
Copyright 2018-2019 DEX Pte. Ltd.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
