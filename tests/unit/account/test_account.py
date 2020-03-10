
import pytest
import secrets
from web3 import Web3

from starfish.account import Account


def test_init(config):
    account = Account(config.accounts[0].as_dict)
    assert(account)
    assert(account.address)

    account = Account(config.accounts[0].as_tuple)
    assert(account)
    assert(account.address)

    account = Account(config.accounts[0].as_list)
    assert(account)
    assert(account.address)

    account = Account(config.accounts[0].address, 'test-password', 'test-keyfie')
    assert(account)
    assert(account.address)

def test_is_address_equal(config):
    account = Account(config.accounts[0].as_dict)
    assert(account.is_address_equal(config.accounts[0].test_address))

def test_is_valid(config):
    account = Account(config.accounts[0].as_dict)
    assert(account.is_valid)

def test_is_password(config):
    account = Account(config.accounts[0].as_dict)
    assert(account.password == config.accounts[0].test_password)

def test_is_keyfile(config):
    account = Account(config.accounts[0].as_dict)
    assert(account.keyfile == config.accounts[0].test_keyfile)

def test_address(config):
    account = Account(config.accounts[0].as_dict)
    assert(account.address.lower() == config.accounts[0].test_address.lower())

def test_as_checksum_address(config):
    account = Account(config.accounts[0].as_dict)
    assert(account.as_checksum_address == Web3.toChecksumAddress(config.accounts[0].test_address))

def test_password(config):
    account = Account(config.accounts[0].as_dict)
    assert(account.password == config.accounts[0].test_password)

def test_set_password(config):
    account = Account(config.accounts[0].as_dict)
    new_password = secrets.token_hex(48)
    account.set_password(new_password)
    assert(account.password != config.accounts[0].test_password)
    assert(account.password == new_password)

