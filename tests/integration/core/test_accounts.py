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


def test_account_load(ocean, config):
    # address only
    account = ocean.load_account(config.publisher_account['address'], config.publisher_account['password'], config.publisher_account['keyfile'])
    assert(account)
    assert(account.address == config.publisher_account['address'])
    assert(account.password == config.publisher_account['password'])
    assert(account.keyfile == config.publisher_account['keyfile'])

def test_account_get_squid_account(ocean, config):
    account = ocean.load_account(config.publisher_account['address'], config.publisher_account['password'], config.publisher_account['keyfile'])
    assert(account)
    squid_account = account.agent_adapter_account
    assert(squid_account)

def test_account_get_balance(ocean, config):
    account = ocean.load_account(config.publisher_account['address'], config.publisher_account['password'], config.publisher_account['keyfile'])
    assert(account)
    account.request_tokens(1)
    assert(account.ocean_balance)
    assert(account.ether_balance)

"""
def test_account_list(ocean, config):
    publisher_account = ocean.get_account(config.publisher_account)
    accounts = ocean.accounts
    assert(len(accounts) > 1)
    assert(publisher_account.is_address_equal((list(accounts)[0])))
"""


