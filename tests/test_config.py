#!/usr/bin/env python
"""

    Tests for `ocean agent command line`.

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
    

