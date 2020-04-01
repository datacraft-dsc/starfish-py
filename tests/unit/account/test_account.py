
import json
import pytest
import secrets
import tempfile
import os

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

    account = Account(config.accounts[0].address, 'test-password', 'test-keyvalue')
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

def test_is_key_value(config):
    account = Account(config.accounts[0].as_dict)
    assert(account.key_value == config.accounts[0].test_key_value)

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


def test_account_key_file():
    test_password = secrets.token_bytes(32)
    account = Account.create(test_password)

    assert(account.password == test_password)
    assert(json.dumps(account.key_value))

    test_filename = '/tmp/key_file.json'
    account.save_to_file(test_filename)
    assert(os.path.exists(test_filename))
    account.load_from_file(test_filename)
    os.unlink(test_filename)

    account.save_to_file(test_filename)
    assert(os.path.exists(test_filename))

    private_key = account.export_key(test_password)
    assert(private_key)

    account.import_key(private_key, test_password)

