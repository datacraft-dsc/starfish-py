#!/usr/bin/env python
"""

    Tests for `starfish-py account`.

"""
import unittest

def test_account_load(config, accounts):
    # address only
    account = accounts[0]
    assert(account)
    assert(account.address.lower() == config.account_1['address'].lower())
    assert(account.password == config.account_1['password'])
    assert(account.keyfile == config.account_1['keyfile'])
