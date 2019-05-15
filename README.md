[![banner](https://raw.githubusercontent.com/oceanprotocol/art/master/github/repo-banner%402x.png)](https://dex.sg)

# starfish-py

Floating on the surface of the Ocean. Ocean-py (Ocean Python) provides user access and tools to the Ocean Protocol Network, via the python library squid-py.

[![Travis (.com)](https://img.shields.io/travis/com/DEX-Company/starfish-py.svg)](https://travis-ci.com/DEX-Company/starfish-py)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/385d72f0a6314b18bedd96e808a90e46)](https://www.codacy.com/app/billbsing/starfish-py?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=DEX-Company/starfish-py&amp;utm_campaign=Badge_Grade)
[![GitHub contributors](https://img.shields.io/github/contributors/DEX-Company/starfish-py.svg)](https://github.com/DEX-Company/starfish-py/graphs/contributors)
[![Squid Version](https://img.shields.io/badge/squid--py-v0.5.13-blue.svg)](https://github.com/oceanprotocol/squid-py/releases/tag/v0.5.13)
[![Barge Version](https://img.shields.io/badge/barge-dex--2019--05--13-blue.svg)](https://github.com/DEX-Company/barge/releases/tag/dex-2019-05-13)

---

## Table of Contents

  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Quickstart](#quickstart)
  - [Environment variables](#environment-variables)
  - [Code style](#code-style)
  - [Testing](#testing)
  - [New Version](#new-version)
  - [License](#license)

---

## Features

Currently only provide basic account balance information

## Prerequisites

Python 3.6

## Development

1. Set up a virtual environment

1. Install requirements

    ```
    pip install -r requirements_dev.txt
    ```

1. Run the unit tests, without any supporting software/libraries outside of starfish

    ```
    python3 -m pytest tests/unit
    ```

1. Create the local testing environment using [barge](https://github.com/DEX-Company/barge).

    In a sepearte terminal session you need to clone and checkout the correct taged
    version of ```barge``` repository, by doing the following:
    ```
    git clone https://github.com/DEX-Company/barge.git
    cd barge
    git checkout tags/dex-2019-05-13
    ./start_ocean.sh --no-brizo --no-pleuston --local-spree-node
    ```

1. Copy keeper artifacts

    A bash script is available to copy keeper artifacts into this file directly from a running docker image. This script needs to run in the root of the project.
    The script waits until the keeper contracts are deployed, and then copies the artifacts.

    ```
    ./scripts/wait_for_migration_and_extract_keeper_artifacts.sh
    ```

    The artifacts contain the addresses of all the deployed contracts and their ABI definitions required to interact with them.

1. Run the integration tests

    ```
    python3 -m pytest tests/integration
    ```

1. Run the all tests

    ```bash
    python3 -m pytest tests

    # or

    python3 setup.py test

    ```

## Documentation

1. Build Sphinx documentation
    To build the Syphinx auto documentation, you need to do the following:
    ```bash
    make docs
    ```

The [documentation](https://shrimp.octet.services/starfish) for this repo is on the starfish doc site [shrimp server](https://shrimp.octet.services).
 
## Code style

The information about code style in python is documented in this two links [python-developer-guide](https://github.com/oceanprotocol/dev-ocean/blob/master/doc/development/python-developer-guide.md)
and [python-style-guide](https://github.com/oceanprotocol/dev-ocean/blob/master/doc/development/python-style-guide.md).

## Testing

Automatic tests are setup via Travis, executing `tox`.
Our test use pytest framework.

## New Version

The `bumpversion.sh` script helps to bump the project version. You can execute the script using as first argument {major|minor|patch} to bump accordingly the version.

## License

```
Copyright 2018 Ocean Protocol Foundation Ltd.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
