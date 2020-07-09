#!/usr/bin/env python
"""

    Tests for `starfish-py account`.

"""
import json
import unittest

def test_account_load(config, accounts):
    # address only
    account = accounts[0]
    assert(account)
    assert(account.address.lower() == config['accounts']['account1']['address'].lower())
    assert(account.password == config['accounts']['account1']['password'])
    with open(config['accounts']['account1']['keyfile'], 'r') as fp:
        key_value = fp.read()
