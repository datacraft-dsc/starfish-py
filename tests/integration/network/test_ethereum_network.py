"""

    Test DNetwork class

"""
import pytest
import secrets

from starfish.utils.did import did_generate_random
from starfish.agent import RemoteAgent
from starfish.agent.services import Services

# from starfish.ethereum_network.ethereum_network import EthereumNetwork

TEST_AMOUNT = 5

def test_network_basic(config, ethereum_network):
    assert(ethereum_network.name)
    assert(ethereum_network.web3)
    assert(ethereum_network.contract_names)
    assert(ethereum_network.url == config['ethereum']['network']['url'])

def test_network_account(ethereum_network, ethereum_accounts):
    test_account = ethereum_accounts[0]
    ether_balance = ethereum_network.get_ether_balance(test_account)
    assert(ether_balance)

    token_balance = ethereum_network.get_token_balance(test_account)
    assert(token_balance)

def test_network_request_test_tokens(ethereum_network, ethereum_accounts):

    test_account = ethereum_accounts[0]

    token_balance = ethereum_network.get_token_balance(test_account)
    assert(token_balance)

    ethereum_network.request_test_tokens(test_account, TEST_AMOUNT)

    new_token_balance = ethereum_network.get_token_balance(test_account)
    assert(new_token_balance)
    assert(token_balance + TEST_AMOUNT == new_token_balance)

def test_network_send_ether(ethereum_network, ethereum_accounts):
    from_account = ethereum_accounts[0]
    to_account = ethereum_accounts[1]

    from_balance = ethereum_network.get_ether_balance(from_account)
    to_balance = ethereum_network.get_ether_balance(to_account)

    receipt = ethereum_network.send_ether(from_account, to_account, TEST_AMOUNT)

    new_from_balance = ethereum_network.get_ether_balance(from_account)
    new_to_balance = ethereum_network.get_ether_balance(to_account)

    assert(int(from_balance) - TEST_AMOUNT == new_from_balance)
    assert(int(to_balance) + TEST_AMOUNT == new_to_balance)


def test_network_send_token(ethereum_network, ethereum_accounts):
    from_account = ethereum_accounts[0]
    to_account = ethereum_accounts[1]

    ethereum_network.request_test_tokens(from_account, TEST_AMOUNT)

    from_balance = ethereum_network.get_token_balance(from_account)
    to_balance = ethereum_network.get_token_balance(to_account)

    receipt = ethereum_network.send_token(from_account, to_account, TEST_AMOUNT)

    new_from_balance = ethereum_network.get_token_balance(from_account)
    new_to_balance = ethereum_network.get_token_balance(to_account)

    assert(from_balance - TEST_AMOUNT == new_from_balance)
    assert(to_balance + TEST_AMOUNT == new_to_balance)

def test_network_send_token_and_log(ethereum_network, ethereum_accounts):
    from_account = ethereum_accounts[0]
    to_account = ethereum_accounts[1]

    ethereum_network.request_test_tokens(from_account, TEST_AMOUNT)

    from_balance = ethereum_network.get_token_balance(from_account)
    to_balance = ethereum_network.get_token_balance(to_account)

    ref_1 = secrets.token_hex(32)
    ref_2 = secrets.token_hex(32)
    receipt = ethereum_network.send_token_and_log(from_account, to_account, TEST_AMOUNT, ref_1, ref_2)

    new_from_balance = ethereum_network.get_token_balance(from_account)
    new_to_balance = ethereum_network.get_token_balance(to_account)

    assert(from_balance - TEST_AMOUNT == new_from_balance)
    assert(to_balance + TEST_AMOUNT == new_to_balance)

    is_sent = ethereum_network.is_token_sent(
        from_account,
        to_account,
        TEST_AMOUNT,
        ref_1,
        ref_2
    )
    assert(is_sent)

def test_network_regiser_provenance(ethereum_network, ethereum_accounts):

    register_account = ethereum_accounts[0]
    asset_id = secrets.token_hex(32)

    ethereum_network.register_provenace(register_account, asset_id)
    event_list = ethereum_network.get_provenace_event_list(asset_id)
    assert(len(event_list) > 0)


def test_network_regiser_resolve_did_ddo(config, ethereum_network, ethereum_accounts):
    did = did_generate_random()

    local_agent = config['agents']['local']
    services = Services(local_agent['url'], all_services=True)
    ddo = RemoteAgent.generate_ddo(services)
    ddo_text = ddo.as_text()

    register_account = ethereum_accounts[0]
    ethereum_network.register_did(register_account, did, ddo_text)

    ddo_text_saved = ethereum_network.resolve_did(did)

    assert(ddo_text == ddo_text_saved)


def test_network_resolve_agent(config, ethereum_network, ethereum_accounts):
    local_agent = config['agents']['local']
    ddo = ethereum_network.resolve_agent(local_agent['url'])

    did = did_generate_random()
    services = Services(local_agent['url'], all_services=True)
    ddo = RemoteAgent.generate_ddo(services)
    ddo_text = ddo.as_text()

    register_account = ethereum_accounts[0]
    ethereum_network.register_did(register_account, did, ddo_text)


    ddo = ethereum_network.resolve_agent(did)
    assert(ddo)

