#!/usr/bin/env python
"""

    Tests for `starfish-py config`.

"""
import unittest
import os
import logging

from squid_py import Ocean as SquidOcean
from squid_py import Config as SquidConfig

from starfish.config import Config
from starfish.logging import setup_logging
from starfish import logger

setup_logging(level=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("web3").setLevel(logging.WARNING)

TEST_VALUES = {

    'contract_path': 'test_contract_path_value',
    'storage_path': 'test storage path value',
    'ocean_url': 'test ocean url',
    'gas_limit': '12233',
    'aquarius_url': 'test aquarius url',
    'brizo_url': 'test brizo url',
    'secret_store_url': 'test secret store url',
    'parity_url': 'test parity url',
}


def test_config_load():

    test_contract_path = 'test_contract_path'
    config = Config(contract_path = test_contract_path)
    assert(config)
    assert(config.contract_path == test_contract_path)

    test_contract_path_env = 'test_contract_path_env'

    os.environ['CONTRACT_PATH'] = test_contract_path_env
    config = Config()
    assert(config)
    assert(config.contract_path == test_contract_path_env)

    config = Config(TEST_VALUES)
    assert(config)
    # remove environ setting
    del os.environ['CONTRACT_PATH']

def test_config_generation_for_squid():
    # start off with the most basic info to connect to ocean using squid-py library

    config = Config(
        {
            'ocean_url': 'http://localhost:8545',
            'contract_path': 'artifacts'
        }
    )
    assert(config)
    squid_config = SquidConfig(options_dict=config.as_squid_dict())
    ocean = SquidOcean(squid_config)
    assert(ocean)
