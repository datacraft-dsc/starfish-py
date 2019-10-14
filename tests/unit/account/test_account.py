
import pytest
import secrets
from web3 import Web3

from starfish.account import account



def test_init(ocean, config):
    account = ocean.load_account(config.accounts[0].as_dict)
    assert(account)
    assert(account.address)

    account = ocean.load_account(config.accounts[0].as_tuple)
    assert(account)
    assert(account.address)

    account = ocean.load_account(config.accounts[0].as_list)
    assert(account)
    assert(account.address)

def test_request_tokens(ocean, config):
    account = ocean.load_account(config.accounts[0].as_dict)
    amount = secrets.randbelow(100) + 1
    assert(account.request_tokens(amount))



def test_is_address_equal(ocean, config):
    account = ocean.load_account(config.accounts[0].as_dict)
    assert(account.is_address_equal(config.accounts[0].test_address))


def test_is_valid(ocean, config):
    account = ocean.load_account(config.accounts[0].as_dict)
    assert(account.is_valid)

def test_is_password(ocean, config):
    account = ocean.load_account(config.accounts[0].as_dict)
    assert(account.password == config.accounts[0].test_password)

def test_is_keyfile(ocean, config):
    account = ocean.load_account(config.accounts[0].as_dict)
    assert(account.keyfile == config.accounts[0].test_keyfile)

def test_address(ocean, config):
    account = ocean.load_account(config.accounts[0].as_dict)
    assert(account.address == config.accounts[0].test_address)

def test_as_checksum_address(ocean, config):
    account = ocean.load_account(config.accounts[0].as_dict)
    assert(account.as_checksum_address == Web3.toChecksumAddress(config.accounts[0].test_address))

def test_password(ocean, config):
    account = ocean.load_account(config.accounts[0].as_dict)
    assert(account.password == config.accounts[0].test_password)


def test_set_password(ocean, config):
    account = ocean.load_account(config.accounts[0].as_dict)
    new_password = secrets.token_hex(48)
    account.set_password(new_password)
    assert(account.password != config.accounts[0].test_password)
    assert(account.password == new_password)


def test_ocean_balance(ocean, config):
    account = ocean.load_account(config.accounts[0].as_dict)
    assert(account.ocean_balance == config.accounts[0].test_tokens)


def test_ether_balance(ocean, config):
    account = ocean.load_account(config.accounts[0].as_dict)
    assert(account.is_valid)
    assert(account.ether_balance == config.accounts[0].test_ether)
