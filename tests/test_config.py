#!/usr/bin/env python
"""

    Tests for `ocean-py config`.

"""
import unittest
import random
import os
import logging

from pytest import (
    mark,
    raises,
)

from ocean_py.config import Config
from squid_py.ocean.ocean import Ocean
from ocean_py.logging import setup_logging
from ocean_py import logger

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
    'parity_address': 'test parity address',
    'parity_password': 'test_password'
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

def test_config_generation_for_squid():
    # start off with the most basic info to connect to ocean using squid-py library
    
    config = Config(
        {
            'ocean_url': 'http://localhost:8545',
            'contract_path': './artifacts'
        }
    )
    assert(config)
    squid_config_file = config.generate_ocean_config_file()
    # ocean = Ocean(config_file=squid_config_file)
    # assert(ocean)
    logger.debug('squid temp config file {}'.format(squid_config_file))

