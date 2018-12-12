[![banner](https://raw.githubusercontent.com/oceanprotocol/art/master/github/repo-banner%402x.png)](https://oceanprotocol.com)

# ocean-py

>    🐳  [Command line tools and interface for squid-py](https://www.elastic.co/) component for (Python).
>    [oceanprotocol.com](https://oceanprotocol.com)

Floating on the surface of the Ocean. Ocean-py (Ocean Python) provides user access and tools to the Ocean Protocol Network, via the python library squid-py.

[![Travis (.com)](https://img.shields.io/travis/com/oceanprotocol/oceandb-elasticsearch-driver.svg)](https://travis-ci.com/oceanprotocol/oceandb-py)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/236520e0c2c94106b29d43731a599d22)](https://www.codacy.com/app/billbsing/ocean-py?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=oceanprotocol/ocean-py&amp;utm_campaign=Badge_Grade)
[![PyPI](https://img.shields.io/pypi/v/ocean-py.svg)](https://pypi.org/project/ocean-py/)
[![GitHub contributors](https://img.shields.io/github/contributors/oceanprotocol/ocean-py.svg)](https://github.com/oceanprotocol/ocean-py/graphs/contributors)

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

1. Run Docker images. Alternatively, set up and run some or all of the corresponding services locally.

    ```
    docker-compose -f ./docker/docker-compose.yml up
    ```

    It runs an Aquarius node and an Ethereum RPC client. For details, read `docker-compose.yml`.

1. Create local configuration file

    ```
    cp config.ini config_local.ini
    ```

   `config_local.ini` is used by unit tests.

1. Copy keeper artifacts

    A bash script is available to copy keeper artifacts into this file directly from a running docker image. This script needs to run in the root of the project.
    The script waits until the keeper contracts are deployed, and then copies the artifacts.

    ```
    ./scripts/wait_for_migration_and_extract_keeper_artifacts.sh
    ```

    The artifacts contain the addresses of all the deployed contracts and their ABI definitions required to interact with them.

1. Run the unit tests

    ```
    python3 setup.py test
    ```

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
