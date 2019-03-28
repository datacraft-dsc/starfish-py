from unittest.mock import Mock
import pytest
import secrets

from starfish.account import Account

def test_ocean_init(ocean, config):
    assert(ocean.keeper_url == config.keeper_url)
    assert(ocean.contracts_path == config.contracts_path)
    assert(ocean.gas_limit == config.gas_limit)

def test_register_update_agent_service(ocean, config):

    account = ocean.get_account(config.accounts[0].as_dict)

    with pytest.raises(TypeError):
        ocean.register_update_agent_service('service-name', 'http://endpoint:8080', None)

    info = ocean.register_update_agent_service('service-name', 'http://endpoint:8080', account)
    assert(info)
    assert(len(info) == 3)
    assert(info[0])
    assert(type(info[1]).__name__ == 'DDO')
    assert(isinstance(info[2], bytes))

def test_search_operations(ocean):
    assert(not ocean.search_operations('test search text') is None)
    assert(len(ocean.search_operations('test search text')) == 0)
    assert(isinstance(ocean.search_operations('test search text'), list))

def test_get_account(ocean, config):
    account = ocean.get_account(config.accounts[0].as_dict)
    assert(account)

def test_accounts(ocean, config):
    accounts = ocean.accounts
    assert(accounts)
    assert(len(accounts) == len(config.accounts))
