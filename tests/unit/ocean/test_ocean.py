from unittest.mock import Mock
import pytest
import secrets

from starfish import Ocean
from starfish.account import Account
from starfish.agent import RemoteAgent

def test_ocean_init(config):
    ocean = Ocean(
        network='nile',
        keeper_url=config.keeper_url,
        contracts_path=config.contracts_path,
        gas_limit=config.gas_limit,
        connect=False
    )
    assert(ocean)
    assert(ocean.keeper_url == config.keeper_url)
    assert(ocean.contracts_path == config.contracts_path)
    assert(ocean.gas_limit == config.gas_limit)

def test_ocean_init_empty(config):
    # now test with no block chain network
    ocean = Ocean()

    assert(ocean)

    account = ocean.load_account(config.accounts[0].address)

    # account should work even if there is no network
    assert( account)

    # error in register since account is in valid
    with pytest.raises(ValueError):
        info = ocean.register_did('did', 'ddo', account)

    assert(not ocean.search_operations('test search text') is None)

    assert(ocean.keeper_url == None)
    assert(ocean.contracts_path == None)
    assert(ocean.gas_limit == 0)


def test_register_update_agent_service(ocean, config):

    account = ocean.load_account(config.accounts[0].as_dict)

    ddo = RemoteAgent.generate_ddo(config.remote_agent_url)
    with pytest.raises(TypeError):
        ocean.register_did(ddo.did, ddo.as_text, None)

    with pytest.raises(TypeError):
        ocean.register_did(ddo.did, {}, account)

    reciept = ocean.register_did(ddo.did, ddo.as_text(), account)
    assert(reciept)

def test_search_operations(ocean):
    assert(not ocean.search_operations('test search text') is None)
    assert(len(ocean.search_operations('test search text')) == 0)
    assert(isinstance(ocean.search_operations('test search text'), list))

def test_load_account(ocean, config):
    account = ocean.load_account(config.accounts[0].as_dict)
    assert(account)

"""
def test_accounts(ocean, config):
    accounts = ocean.accounts
    assert(accounts)
    assert(len(accounts) == len(config.accounts))
"""

def test_ocean_properties(ocean, config):
    assert(ocean.keeper_url == config.keeper_url)
    assert(ocean.contracts_path == config.contracts_path)
    assert(ocean.gas_limit == config.gas_limit)
