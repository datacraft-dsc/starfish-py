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
    assert(account.is_valid)

def test_account_get_balance(ocean, config):
    account = ocean.get_account(config.publisher_account)
    assert(account)
    assert(account.unlock())
    account.request_tokens(1)
    assert(account.ocean_balance)
    assert(account.ether_balance)

def test_account_list(ocean, config):
    publisher_account = ocean.get_account(config.publisher_account)
    accounts = ocean.accounts
    assert(len(accounts) > 1)
    assert(publisher_account.is_address_equal((list(accounts)[0])))

def test_account_creation(ocean):
    password = secrets.token_hex(120)
    account = ocean.create_account(password)
    assert(account)
