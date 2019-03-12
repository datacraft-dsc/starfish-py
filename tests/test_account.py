#!/usr/bin/env python
"""

    Tests for `starfish-py account`.

"""
import unittest
import os
import logging

from starfish import Ocean
from squid_py import Ocean as SquidOcean
from squid_py import Config as SquidConfig

CONFIG_PARAMS = {'contracts_path': 'artifacts', 'keeper_url': 'http://localhost:8545' }
PUBLISHER_ACCOUNT = { 'address': '0x00bd138abd70e2f00903268f3db08f2d25677c9e', 'password': 'node0'}


def test_account_load():
    ocean = Ocean(CONFIG_PARAMS, log_level=logging.DEBUG)
    account = ocean.get_account(PUBLISHER_ACCOUNT['address'])
    assert account
    assert account.address == PUBLISHER_ACCOUNT['address']
    assert account.password is None

    account = ocean.get_account(PUBLISHER_ACCOUNT)
    assert account
    assert account.address == PUBLISHER_ACCOUNT['address']
    assert account.password == PUBLISHER_ACCOUNT['password']

def test_account_get_squid_account():
    ocean = Ocean(CONFIG_PARAMS)
    account = ocean.get_account(PUBLISHER_ACCOUNT)
    assert account
    squid_account = account._squid_account
    assert squid_account
    assert account.is_valid


def test_account_get_balance():
    ocean = Ocean(CONFIG_PARAMS)
    account = ocean.get_account(PUBLISHER_ACCOUNT)
    assert account
    assert account.unlock()
    account.request_tokens(1)
    assert account.ocean_balance
    assert account.ether_balance

def test_account_list():
    ocean = Ocean(CONFIG_PARAMS)
    publisher_account = ocean.get_account(PUBLISHER_ACCOUNT)
    accounts = ocean.accounts
    assert len(accounts) > 1
    assert publisher_account.is_address_equal((list(accounts)[0]))
