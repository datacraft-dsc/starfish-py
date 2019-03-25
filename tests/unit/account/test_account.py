
import pytest
import secrets


from starfish.account import account
from tests.unit.test_config import testConfig



def test_init(ocean):
    account = ocean.get_account(testConfig.accounts[0].as_dict)
    assert(account)
    assert(account.address)
    
    account = ocean.get_account(testConfig.accounts[0].as_tuple)
    assert(account)
    assert(account.address)

    account = ocean.get_account(testConfig.accounts[0].as_list)
    assert(account)
    assert(account.address)

def test_unlock(ocean):
    account = ocean.get_account(testConfig.accounts[0].as_dict)
    assert(account.unlock())

def test_lock(ocean):
    account = ocean.get_account(testConfig.accounts[0].as_dict)
    assert(account.unlock())
    assert(account.lock())


def test_request_tokens(ocean):
    account = ocean.get_account(testConfig.accounts[0].as_dict)
    amount = secrets.randbelow(100)

    with pytest.raises(ValueError, match='You must unlock' ):
        account.request_tokens(amount)
    account.unlock()
    assert(account.request_tokens(amount))



def test_is_address_equal(ocean):
    account = ocean.get_account(testConfig.accounts[0].as_dict)
    assert(account.is_address_equal(testConfig.accounts[0].test_address))


def test_is_valid(ocean):
    account = ocean.get_account(testConfig.accounts[0].as_dict)
    assert(account.is_valid)

def test_is_password(ocean):
    account = ocean.get_account(testConfig.accounts[0].as_dict)
    assert(account.password == testConfig.accounts[0].test_password)

def test_address(ocean):
    account = ocean.get_account(testConfig.accounts[0].as_dict)
    assert(account.address == testConfig.accounts[0].test_address)

def test_as_checksum_address(ocean):
    account = ocean.get_account(testConfig.accounts[0].as_dict)
    assert(account.as_checksum_address == ocean._web3.toChecksumAddress(testConfig.accounts[0].test_address))

def test_password(ocean):
    account = ocean.get_account(testConfig.accounts[0].as_dict)
    assert(account.password == testConfig.accounts[0].test_password)


def test_set_password(ocean):
    account = ocean.get_account(testConfig.accounts[0].as_dict)
    new_password = secrets.token_hex(48)
    account.set_password(new_password)
    assert(account.password != testConfig.accounts[0].test_password)
    assert(account.password == new_password)


def test_ocean_balance(ocean):
    account = ocean.get_account(testConfig.accounts[0].as_dict)
    assert(account.ocean_balance == testConfig.accounts[0].test_tokens)


def test_ether_balance(ocean):
    account = ocean.get_account(testConfig.accounts[0].as_dict)
    print(testConfig.accounts[0].as_dict)
    assert(account.is_valid)
    assert(account.ether_balance == testConfig.accounts[0].test_ether)
