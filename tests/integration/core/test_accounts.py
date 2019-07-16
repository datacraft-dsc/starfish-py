#!/usr/bin/env python
"""

    Tests for `starfish-py account`.

"""
import unittest
import os
import logging
import secrets

from starfish import Ocean, logger
from squid_py import Ocean as SquidOcean
from squid_py import Config as SquidConfig
from squid_py.keeper.web3_provider import Web3Provider


def test_account_load(ocean, config):
    # address only
    account = ocean.get_account(config.publisher_account['address'])
    assert(account)
    assert(account.address == config.publisher_account['address'])
    assert(account.password is None)

    # address and password as a tuple
    account = ocean.get_account(config.publisher_account)
    assert(account)
    assert(account.address == config.publisher_account['address'])
    assert(account.password == config.publisher_account['password'])

def test_account_get_squid_account(ocean, config):
    account = ocean.get_account(config.publisher_account)
    assert(account)
    squid_account = account._squid_account
    assert(squid_account)
    assert(account.is_hosted)

def test_account_get_balance(ocean, config):
    account = ocean.get_account(config.publisher_account)
    assert(account)
    assert(account.unlock())
    account.request_tokens(1)
    assert(account.ocean_balance)
    assert(account.ether_balance)
    print(account.ether_balance)

def test_account_list(ocean, config):
    publisher_account = ocean.get_account(config.publisher_account)
    accounts = ocean.accounts
    assert(len(accounts) > 1)
    assert(publisher_account.is_address_equal((list(accounts)[0])))

def _disable_test_account_creation_and_transfer(ocean, config):
    password = secrets.token_hex(120)
    account = ocean.create_account(password)
    assert(account)
    found_account = ocean.get_account(account.address)

    assert(found_account)

    search_account = None
    for address in ocean.accounts:
        if account.address == address:
            search_account = address
    assert(search_account)
    assert(account.ether_balance == 0)
    assert(account.ocean_balance == 0)

    # test ether transfer
    publisher_account = ocean.get_account(config.publisher_account)
    publisher_account.unlock()
    publisher_account.transfer_ether(account.address, 3)
    assert(account.ether_balance == 3)

    # test ocean token request
    account.unlock()
    account.request_tokens(7)
    assert(account.ocean_balance == 7)

    # test transfer ocean tokens
    publisher_account = ocean.get_account(config.publisher_account)
    publisher_account.unlock()
    publisher_account.transfer_token(account.address, 5)
    assert(account.ocean_balance == 12)



