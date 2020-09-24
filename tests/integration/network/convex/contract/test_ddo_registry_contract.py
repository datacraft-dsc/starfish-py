"""

    Test Convex ddo register contract for starfish

"""

import pytest
import secrets
from tests.integration.network.convex.helpers import auto_topup_account

from convex_api.account import Account
from convex_api.convex_api import ConvexAPI
from convex_api.exceptions import ConvexAPIError

from starfish.network.convex.contract.ddo_registry_contract import (
    CONTRACT_NAME,
    CONTRACT_VERSION,
    ddo_registry_contract
)

# (import convex.trust :as trust)



ddo_register_contract_address = None

@pytest.fixture
def contract_address(convex_network, convex_accounts):
    global ddo_register_contract_address
    test_account = convex_accounts[0]
    auto_topup_account(convex_network, test_account, 50000000)
    if ddo_register_contract_address is None:
        result = convex_network.convex.send(ddo_registry_contract, test_account)
        assert(result['value'])
        auto_topup_account(convex_network, test_account)
        ddo_register_contract_address = result['value']
    return ddo_register_contract_address


def test_contract_version(convex_network, convex_accounts, contract_address):
    test_account = convex_accounts[0]
    command = f'(call {contract_address} (version))'
    result = convex_network.convex.query(command, test_account)
    assert(result['value'])
    assert(result['value'] == CONTRACT_VERSION)

def test_contract_did_register_assert_did(convex_network, convex_accounts, contract_address):

    test_account = convex_accounts[0]
    auto_topup_account(convex_network, test_account)

    did_bad = secrets.token_hex(20)
    did_valid = secrets.token_hex(32)
    ddo = 'test - ddo'
    command = f'(call {contract_address} (register "{did_bad}" "{ddo}"))'
    with pytest.raises(ConvexAPIError, match='INVALID'):
        result = convex_network.convex.send(command, test_account)

    command = f'(call {contract_address} (register "" "{ddo}"))'
    with pytest.raises(ConvexAPIError, match='INVALID'):
        result = convex_network.convex.send(command, test_account)

    command = f'(call {contract_address} (register 42 "{ddo}"))'
    with pytest.raises(ConvexAPIError, match='INVALID'):
        result = convex_network.convex.send(command, test_account)

    command = f'(call {contract_address} (register 0x{did_valid} "{ddo}"))'
    result = convex_network.convex.send(command, test_account)
    assert(result['value'])
    assert(result['value'] == f'0x{did_valid}')


def test_contract_did_register_resolve(convex_network, convex_accounts, contract_address):

    test_account = convex_accounts[0]
    other_account = convex_accounts[1]

    auto_topup_account(convex_network, convex_accounts)

    did = f'0x{secrets.token_hex(32)}'
    ddo = 'test - ddo'


    # call register

    command = f'(call {contract_address} (register {did} "{ddo}"))'
    result = convex_network.convex.send(command, test_account)
    assert(result['value'])
    assert(result['value'] == did)

    # call resolve did to ddo

    command = f'(call {contract_address} (resolve {did}))'
    result = convex_network.convex.query(command, test_account)
    assert(result['value'])
    assert(result['value'] == ddo)

    # call resolve did to ddo on other account

    command = f'(call {contract_address} (resolve {did}))'
    result = convex_network.convex.query(command, other_account)
    assert(result['value'])
    assert(result['value'] == ddo)

    # call owner? on owner account
    command = f'(call {contract_address} (owner? {did}))'
    result = convex_network.convex.query(command, test_account)
    assert(result['value'])

    # call owner? on owner other_account
    command = f'(call {contract_address} (owner? {did}))'
    result = convex_network.convex.query(command, other_account)
    assert(not result['value'])

    # call resolve unknown
    bad_did = f'0x{secrets.token_hex(32)}'
    command = f'(call {contract_address} (resolve {bad_did}))'
    result = convex_network.convex.query(command, test_account)
    assert(result['value'] == '')


    new_ddo = 'new - ddo'
    # call register - update

    command = f'(call {contract_address} (register {did} "{new_ddo}"))'
    result = convex_network.convex.send(command, test_account)
    assert(result['value'])
    assert(result['value'] == did)


    # call register - update from other account

    with pytest.raises(ConvexAPIError, match='NOT-OWNER'):
        command = f'(call {contract_address} (register {did} "{ddo}"))'
        result = convex_network.convex.send(command, other_account)


    # call resolve did to new_ddo

    command = f'(call {contract_address} (resolve {did}))'
    result = convex_network.convex.query(command, test_account)
    assert(result['value'])
    assert(result['value'] == new_ddo)


    # call unregister fail - from other account

    with pytest.raises(ConvexAPIError, match='NOT-OWNER'):
        command = f'(call {contract_address} (unregister {did}))'
        result = convex_network.convex.send(command, other_account)


    # call unregister

    command = f'(call {contract_address} (unregister {did}))'
    result = convex_network.convex.send(command, test_account)
    assert(result['value'])
    assert(result['value'] == did)

    # call resolve did to empty

    command = f'(call {contract_address} (resolve {did}))'
    result = convex_network.convex.query(command, test_account)
    assert(result['value'] == '')


    # call unregister - unknown did

    command = f'(call {contract_address} (unregister {bad_did}))'
    result = convex_network.convex.send(command, test_account)
    assert(result['value'] == '')



def test_contract_ddo_transfer(convex_network, convex_accounts):
    # register and transfer

    test_account = convex_accounts[0]
    other_account = convex_accounts[1]
    auto_topup_account(convex_network, convex_accounts)


    contract_address = convex_network.convex.get_address(CONTRACT_NAME, test_account)
    assert(contract_address)

    did = f'0x{secrets.token_hex(32)}'
    ddo = 'test - ddo'

    command = f'(call {contract_address} (register {did} "{ddo}"))'
    result = convex_network.convex.send(command, test_account)
    assert(result['value'])
    assert(result['value'] == did)

    # call owner? on owner account
    command = f'(call {contract_address} (owner? {did}))'
    result = convex_network.convex.query(command, test_account)
    assert(result['value'])

    # call owner? on other_account
    command = f'(call {contract_address} (owner? {did}))'
    result = convex_network.convex.query(command, other_account)
    assert(not result['value'])


    command = f'(call {contract_address} (transfer {did} {other_account.address_checksum}))'
    result = convex_network.convex.send(command, test_account)
    assert(result['value'])
    assert(result['value'][0] == did)

    #check ownership to different accounts

    # call owner? on owner account
    command = f'(call {contract_address} (owner? {did}))'
    result = convex_network.convex.query(command, test_account)
    assert(not result['value'])

    # call owner? on other_account
    command = f'(call {contract_address} (owner? {did}))'
    result = convex_network.convex.query(command, other_account)
    assert(result['value'])

    # call unregister fail - from test_account (old owner)

    with pytest.raises(ConvexAPIError, match='NOT-OWNER'):
        command = f'(call {contract_address} (unregister {did}))'
        result = convex_network.convex.send(command, test_account)


    # call unregister from other_account ( new owner )

    command = f'(call {contract_address} (unregister {did}))'
    result = convex_network.convex.send(command, other_account)
    assert(result['value'])
    assert(result['value'] == did)

def test_contract_ddo_bulk_register(convex_network, convex_accounts):
    test_account = convex_accounts[0]
    contract_address = convex_network.convex.get_address(CONTRACT_NAME, test_account)
    assert(contract_address)

    for index in range(0, 2):
        auto_topup_account(convex_network, test_account, 40000000)
        did = f'0x{secrets.token_hex(32)}'
#        ddo = secrets.token_hex(51200)
        ddo = secrets.token_hex(1024)

        command = f'(call {contract_address} (register {did} "{ddo}"))'
        result = convex_network.convex.send(command, test_account)
        assert(result['value'])
        assert(result['value'] == did)

def test_contract_ddo_owner_list(convex_network, convex_accounts):

    test_account = convex_accounts[0]
    other_account = convex_accounts[1]
    auto_topup_account(convex_network, convex_accounts)

    contract_address = convex_network.convex.get_address(CONTRACT_NAME, test_account)
    assert(contract_address)

    did_list = []
    for index in range(0, 4):
        auto_topup_account(convex_network, test_account)
        did = f'0x{secrets.token_hex(32)}'
        did_list.append(did)
#        ddo = secrets.token_hex(51200)
        ddo = f'ddo test - {index}'

        command = f'(call {contract_address} (register {did} "{ddo}"))'
        result = convex_network.convex.send(command, test_account)
        assert(result['value'])
        assert(result['value'] == did)


    command = f'(call {contract_address} (owner-list "{test_account.address_api}"))'
    result = convex_network.convex.query(command, test_account)
    assert(result['value'])
    for did in did_list:
        assert(did in result['value'])

