"""

    Test DNetwork class

"""
import pytest
import secrets

from starfish.utils.did import did_generate_random
from starfish.agent import RemoteAgent
from starfish.agent.services import Services

from starfish import DNetwork

TEST_AMOUNT = 5

def test_dnetwork_basic(dnetwork):
    assert(dnetwork.network_name)
    assert(dnetwork.web3)
    assert(dnetwork.contract_names)
    assert(dnetwork.network_url)

def test_dnetwork_account(dnetwork, starfish_accounts):
    test_account = starfish_accounts[0]
    ether_balance = dnetwork.get_ether_balance(test_account)
    assert(ether_balance)

    token_balance = dnetwork.get_token_balance(test_account)
    assert(token_balance)

def test_dnetwork_request_test_tokens(dnetwork, starfish_accounts):

    test_account = starfish_accounts[0]

    token_balance = dnetwork.get_token_balance(test_account)
    assert(token_balance)

    dnetwork.request_test_tokens(test_account, TEST_AMOUNT)

    new_token_balance = dnetwork.get_token_balance(test_account)
    assert(new_token_balance)
    assert(token_balance + TEST_AMOUNT == new_token_balance)

def test_dnetwork_send_ether(dnetwork, starfish_accounts):
    from_account = starfish_accounts[0]
    to_account = starfish_accounts[1]

    from_balance = dnetwork.get_ether_balance(from_account)
    to_balance = dnetwork.get_ether_balance(to_account)

    receipt = dnetwork.send_ether(from_account, to_account, TEST_AMOUNT)

    new_from_balance = dnetwork.get_ether_balance(from_account)
    new_to_balance = dnetwork.get_ether_balance(to_account)

    assert(from_balance - TEST_AMOUNT == new_from_balance)
    assert(to_balance + TEST_AMOUNT == new_to_balance)


def test_dnetwork_send_token(dnetwork, starfish_accounts):
    from_account = starfish_accounts[0]
    to_account = starfish_accounts[1]

    from_balance = dnetwork.get_token_balance(from_account)
    to_balance = dnetwork.get_token_balance(to_account)

    receipt = dnetwork.send_token(from_account, to_account, TEST_AMOUNT)

    new_from_balance = dnetwork.get_token_balance(from_account)
    new_to_balance = dnetwork.get_token_balance(to_account)

    assert(from_balance - TEST_AMOUNT == new_from_balance)
    assert(to_balance + TEST_AMOUNT == new_to_balance)

def test_dnetwork_send_token_and_log(dnetwork, starfish_accounts):
    from_account = starfish_accounts[0]
    to_account = starfish_accounts[1]

    from_balance = dnetwork.get_token_balance(from_account)
    to_balance = dnetwork.get_token_balance(to_account)

    ref_1 = secrets.token_hex(32)
    ref_2 = secrets.token_hex(32)
    receipt = dnetwork.send_token_and_log(from_account, to_account, TEST_AMOUNT, ref_1, ref_2)


    new_from_balance = dnetwork.get_token_balance(from_account)
    new_to_balance = dnetwork.get_token_balance(to_account)

    assert(from_balance - TEST_AMOUNT == new_from_balance)
    assert(to_balance + TEST_AMOUNT == new_to_balance)

    is_sent = dnetwork.is_token_sent(
        from_account,
        to_account,
        TEST_AMOUNT,
        ref_1,
        ref_2
    )
    assert(is_sent)

def test_dnetwork_regiser_provenance(dnetwork, starfish_accounts):

    register_account = starfish_accounts[0]
    asset_id = secrets.token_hex(32)

    dnetwork.register_provenace(register_account, asset_id)
    event_list = dnetwork.get_provenace_event_list(asset_id)
    assert(len(event_list) > 0)


def test_dnetwork_regiser_resolve_did_ddo(config, dnetwork, starfish_accounts):
    did = did_generate_random()

    services = Services(config.remote_agent_url, all_services=True)
    ddo = RemoteAgent.generate_ddo(services)
    ddo_text = ddo.as_text()

    register_account = starfish_accounts[0]
    dnetwork.register_did(register_account, did, ddo_text)

    ddo_text_saved = dnetwork.resolve_did(did)

    assert(ddo_text == ddo_text_saved)





