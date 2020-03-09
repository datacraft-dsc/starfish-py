"""

    Test DNetwork class

"""
import pytest


from starfish import DNetwork

TEST_REQUEST_TOKEN_AMOUNT = 5

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

    dnetwork.request_test_tokens(TEST_REQUEST_TOKEN_AMOUNT, test_account)

    new_token_balance = dnetwork.get_token_balance(test_account)
    assert(new_token_balance)
    assert(token_balance + TEST_REQUEST_TOKEN_AMOUNT == new_token_balance)

def test_dnetwork_send_ether(dnetwork, starfish_accounts):
    from_account = starfish_accounts[0]
    to_account = starfish_accounts[1]
