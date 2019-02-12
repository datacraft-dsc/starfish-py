#!/usr/bin/env python
"""

    Tests for `starfish-py account`.

"""
import unittest
import os
import logging

from starfish import Ocean
from starfish import Config as OceanConfig
from starfish.logging import setup_logging
from starfish import logger
from squid_py import Ocean as SquidOcean
from squid_py import Config as SquidConfig

setup_logging(level=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("web3").setLevel(logging.WARNING)

PUBLISHER_ACCOUNT = { 'address': '0x00bd138abd70e2f00903268f3db08f2d25677c9e', 'password': 'node0'}


def test_account_load():
    ocean = Ocean()
    account = ocean.get_account(PUBLISHER_ACCOUNT['address'])
    assert account
    assert account.address == PUBLISHER_ACCOUNT['address']
    assert account.password is None

    account = ocean.get_account(PUBLISHER_ACCOUNT)
    assert account
    assert account.address == PUBLISHER_ACCOUNT['address']
    assert account.password == PUBLISHER_ACCOUNT['password']

def test_account_get_squid_account():
    ocean = Ocean()
    account = ocean.get_account(PUBLISHER_ACCOUNT)
    assert account
    squid_account = account._squid_account
    assert squid_account
    assert account.is_valid


def test_account_get_balance():
    ocean = Ocean()
    account = ocean.get_account(PUBLISHER_ACCOUNT)
    assert account
    account.request_tokens(1)
    assert account.ocean_balance
    assert account.ether_balance

def test_account_list():
    ocean = Ocean()
    publisher_account = ocean.get_account(PUBLISHER_ACCOUNT)
    accounts = ocean.accounts
    assert len(accounts) > 1
    assert publisher_account.is_address_equal((list(accounts)[0]))
