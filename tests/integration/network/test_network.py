"""

    Test DNetwork class

"""
import pytest
import secrets

from starfish.utils.did import did_generate_random
from starfish.agent import RemoteAgent
from starfish.agent.services import Services

from starfish import Network

TEST_AMOUNT = 5

def test_network_basic(config, network):
    assert(network.name)
    assert(network.web3)
    assert(network.contract_names)
    assert(network.url == config['network']['url'])

def test_network_account(network, accounts):
    test_account = accounts[0]
    ether_balance = network.get_ether_balance(test_account)
    assert(ether_balance)

    token_balance = network.get_token_balance(test_account)
    assert(token_balance)

def test_network_request_test_tokens(network, accounts):

    test_account = accounts[0]

    token_balance = network.get_token_balance(test_account)
    assert(token_balance)

    network.request_test_tokens(test_account, TEST_AMOUNT)

    new_token_balance = network.get_token_balance(test_account)
    assert(new_token_balance)
    assert(token_balance + TEST_AMOUNT == new_token_balance)

def test_network_send_ether(network, accounts):
    from_account = accounts[0]
    to_account = accounts[1]

    from_balance = network.get_ether_balance(from_account)
    to_balance = network.get_ether_balance(to_account)

    receipt = network.send_ether(from_account, to_account, TEST_AMOUNT)

    new_from_balance = network.get_ether_balance(from_account)
    new_to_balance = network.get_ether_balance(to_account)

    assert(int(from_balance) - TEST_AMOUNT == new_from_balance)
    assert(int(to_balance) + TEST_AMOUNT == new_to_balance)


def test_network_send_token(network, accounts):
    from_account = accounts[0]
    to_account = accounts[1]

    network.request_test_tokens(from_account, TEST_AMOUNT)

    from_balance = network.get_token_balance(from_account)
    to_balance = network.get_token_balance(to_account)

    receipt = network.send_token(from_account, to_account, TEST_AMOUNT)

    new_from_balance = network.get_token_balance(from_account)
    new_to_balance = network.get_token_balance(to_account)

    assert(from_balance - TEST_AMOUNT == new_from_balance)
    assert(to_balance + TEST_AMOUNT == new_to_balance)

def test_network_send_token_and_log(network, accounts):
    from_account = accounts[0]
    to_account = accounts[1]

    network.request_test_tokens(from_account, TEST_AMOUNT)

    from_balance = network.get_token_balance(from_account)
    to_balance = network.get_token_balance(to_account)

    ref_1 = secrets.token_hex(32)
    ref_2 = secrets.token_hex(32)
    receipt = network.send_token_and_log(from_account, to_account, TEST_AMOUNT, ref_1, ref_2)

    new_from_balance = network.get_token_balance(from_account)
    new_to_balance = network.get_token_balance(to_account)

    assert(from_balance - TEST_AMOUNT == new_from_balance)
    assert(to_balance + TEST_AMOUNT == new_to_balance)

    is_sent = network.is_token_sent(
        from_account,
        to_account,
        TEST_AMOUNT,
        ref_1,
        ref_2
    )
    assert(is_sent)

def test_network_regiser_provenance(network, accounts):

    register_account = accounts[0]
    asset_id = secrets.token_hex(32)

    network.register_provenace(register_account, asset_id)
    event_list = network.get_provenace_event_list(asset_id)
    assert(len(event_list) > 0)


def test_network_regiser_resolve_did_ddo(config, network, accounts):
    did = did_generate_random()

    local_agent = config['agents']['local']
    services = Services(local_agent['url'], all_services=True)
    ddo = RemoteAgent.generate_ddo(services)
    ddo_text = ddo.as_text()

    register_account = accounts[0]
    network.register_did(register_account, did, ddo_text)

    ddo_text_saved = network.resolve_did(did)

    assert(ddo_text == ddo_text_saved)


def test_network_resolve_agent(config, network, accounts):
    local_agent = config['agents']['local']
    ddo = network.resolve_agent(local_agent['url'])

    did = did_generate_random()
    services = Services(local_agent['url'], all_services=True)
    ddo = RemoteAgent.generate_ddo(services)
    ddo_text = ddo.as_text()

    register_account = accounts[0]
    network.register_did(register_account, did, ddo_text)


    ddo = network.resolve_agent(did)
    assert(ddo)

