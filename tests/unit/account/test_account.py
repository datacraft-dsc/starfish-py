
import pytest
import secrets


from starfish.account import account



def test_init(ocean, config):
    account = ocean.get_account(config.accounts[0].as_dict)
    assert(account)
    assert(account.address)
    
    account = ocean.get_account(config.accounts[0].as_tuple)
    assert(account)
    assert(account.address)

    account = ocean.get_account(config.accounts[0].as_list)
    assert(account)
    assert(account.address)

def test_unlock(ocean, config):
    account = ocean.get_account(config.accounts[0].as_dict)
    assert(account.unlock())

def test_lock(ocean, config):
    account = ocean.get_account(config.accounts[0].as_dict)
    assert(account.unlock())
    assert(account.lock())


def test_request_tokens(ocean, config):
    account = ocean.get_account(config.accounts[0].as_dict)
    amount = secrets.randbelow(100)

    with pytest.raises(ValueError, match='You must unlock' ):
        account.request_tokens(amount)
    account.unlock()
    assert(account.request_tokens(amount))



def test_is_address_equal(ocean, config):
    account = ocean.get_account(config.accounts[0].as_dict)
    assert(account.is_address_equal(config.accounts[0].test_address))


def test_is_valid(ocean, config):
    account = ocean.get_account(config.accounts[0].as_dict)
    assert(account.is_valid)

def test_is_password(ocean, config):
    account = ocean.get_account(config.accounts[0].as_dict)
    assert(account.password == config.accounts[0].test_password)

def test_address(ocean, config):
    account = ocean.get_account(config.accounts[0].as_dict)
    assert(account.address == config.accounts[0].test_address)

def test_as_checksum_address(ocean, config):
    account = ocean.get_account(config.accounts[0].as_dict)
    assert(account.as_checksum_address == ocean._web3.toChecksumAddress(config.accounts[0].test_address))

def test_password(ocean, config):
    account = ocean.get_account(config.accounts[0].as_dict)
    assert(account.password == config.accounts[0].test_password)


def test_set_password(ocean, config):
    account = ocean.get_account(config.accounts[0].as_dict)
    new_password = secrets.token_hex(48)
    account.set_password(new_password)
    assert(account.password != config.accounts[0].test_password)
    assert(account.password == new_password)


def test_ocean_balance(ocean, config):
    account = ocean.get_account(config.accounts[0].as_dict)
    assert(account.ocean_balance == config.accounts[0].test_tokens)


def test_ether_balance(ocean, config):
    account = ocean.get_account(config.accounts[0].as_dict)
    assert(account.is_valid)
    assert(account.ether_balance == config.accounts[0].test_ether)