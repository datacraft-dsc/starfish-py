from unittest.mock import Mock
import pytest
import secrets

from starfish.account import Account
from tests.unit.test_config import testConfig

def test_ocean_init(ocean):
    assert(ocean.keeper_url == testConfig.keeper_url)
    assert(ocean.contracts_path == testConfig.contracts_path)
    assert(ocean.gas_limit == testConfig.gas_limit)

def test_register_update_agent_service(ocean):

    account = ocean.get_account(testConfig.accounts[0])

    with pytest.raises(TypeError):
        ocean.register_update_agent_service('service-name', 'http://endpoint:8080', None)

    info = ocean.register_update_agent_service('service-name', 'http://endpoint:8080', account)
    assert(info)
    assert(info[0])
    assert(type(info[1]).__name__ == 'DDO')
    assert(isinstance(info[2], bytes))

def test_search_operations(ocean):
    assert(not ocean.search_operations('test search text') is None)
    assert(len(ocean.search_operations('test search text')) == 0)
    assert(isinstance(ocean.search_operations('test search text'), list))

def test_get_account(ocean):
    account = ocean.get_account(testConfig.accounts[0])
    assert(account)

def test_accounts(ocean):
    accounts = ocean.accounts
    assert(accounts)
    assert(len(accounts) == len(testConfig.accounts))
