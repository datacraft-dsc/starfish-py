
import json
import pytest
import secrets
import tempfile
import os

from web3 import Web3

from starfish.network.ethereum_account import EthereumAccount


def test_init(config):
    account = EthereumAccount(config.ethereum.accounts[0].password, config.ethereum.accounts[0].key_data)
    assert(account)
    assert(account.address)

def test_is_address_equal(config):
    account = EthereumAccount(config.ethereum.accounts[0].password, config.ethereum.accounts[0].key_data)
    assert(account.is_address_equal(config.ethereum.accounts[0].address))

def test_is_valid(config):
    account = EthereumAccount(config.ethereum.accounts[0].password, config.ethereum.accounts[0].key_data)
    assert(account.is_valid)

def test_is_password(config):
    account = EthereumAccount(config.ethereum.accounts[0].password, config.ethereum.accounts[0].key_data)
    assert(account.password == config.ethereum.accounts[0].password)

def test_is_key_data(config):
    account = EthereumAccount(config.ethereum.accounts[0].password, config.ethereum.accounts[0].key_data)
    assert(account.key_data == config.ethereum.accounts[0].key_data)

def test_address(config):
    account = EthereumAccount(config.ethereum.accounts[0].password, config.ethereum.accounts[0].key_data)
    assert(account.address.lower() == config.ethereum.accounts[0].address.lower())

def test_as_checksum_address(config):
    account = EthereumAccount(config.ethereum.accounts[0].password, config.ethereum.accounts[0].key_data)
    assert(account.as_checksum_address == Web3.toChecksumAddress(config.ethereum.accounts[0].address))

def test_password(config):
    account = EthereumAccount(config.ethereum.accounts[0].password, config.ethereum.accounts[0].key_data)
    assert(account.password == config.ethereum.accounts[0].password)

def test_account_key_file():
    test_password = secrets.token_bytes(32)
    account = EthereumAccount.create(test_password)

    assert(account.password == test_password)
    assert(json.dumps(account.key_data))

    test_filename = '/tmp/key_file.json'
    account.save_to_file(test_filename)
    assert(os.path.exists(test_filename))
    account.load_from_file(test_filename)
    os.unlink(test_filename)

    account.save_to_file(test_filename)
    assert(os.path.exists(test_filename))

    private_key = account.export_private_key(test_password)
    assert(private_key)

    account.import_key(private_key, test_password)

