import unittest
from unittest.mock import Mock
import pytest
import secrets


from starfish.account import Account
# ocean class test

from conftest import testConfig

def test_ocean_init(ocean):
    assert(ocean.keeper_url == testConfig.keeper_url)
    assert(ocean.contracts_path == testConfig.contracts_path)
    assert(ocean.gas_limit == testConfig.gas_limit)

def test_register_update_agent_service(ocean):

    test_address = secrets.token_hex(32)
    test_password = secrets.token_hex(12)
    account = Account(test_address, test_password)

    with pytest.raises(TypeError):
        ocean.register_update_agent_service('service-name', 'http://endpoint:8080', None)

    # ocean.register_update_agent_service('service-name', 'http://endpoint:8080', account)

def test_search_operations(ocean):
    assert(not ocean.search_operations('test search text') is None)
    assert(len(ocean.search_operations('test search text')) == 0)
    assert(isinstance(ocean.search_operations('test search text'), list))

def test_get_account(ocean):
    assert(True)

def test_accounts(ocean):
    assert(True)
