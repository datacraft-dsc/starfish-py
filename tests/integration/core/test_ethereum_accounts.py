#!/usr/bin/env python
"""

    Tests for `starfish-py account`.

"""
import json
import unittest

def test_ethereum_account_load(config, ethereum_accounts):
    # address only
    account = ethereum_accounts[0]
    assert(account)
    assert(account.address.lower() == config['ethereum']['accounts']['account1']['address'].lower())
    assert(account.password == config['ethereum']['accounts']['account1']['password'])
    with open(config['ethereum']['accounts']['account1']['keyfile'], 'r') as fp:
        key_value = fp.read()
