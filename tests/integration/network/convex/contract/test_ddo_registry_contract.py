"""

    Test Convex ddo register contract for starfish

"""

import datetime
import json
import pytest
import secrets
from tests.integration.network.convex.helpers import auto_topup_account

from convex_api.account import Account
from convex_api.convex_api import ConvexAPI
from convex_api.exceptions import ConvexAPIError

from starfish.network.convex.contract.ddo_registry_contract import DDORegistryContract
from starfish.network.convex.contract.contract_manager import CONTRACT_ACCOUNTS

# (import convex.trust :as trust)


def test_contract_did_register_methods(convex_network, convex_accounts):

    deploy_address = CONTRACT_ACCOUNTS['development']
    register_account = convex_accounts[1]
    auto_topup_account(convex_network, register_account)
    query_address = register_account.address_checksum

    did = f'0x{secrets.token_hex(32)}'
    ddo = f'test - ddo - {did}'

    contract = DDORegistryContract(convex_network.convex)
    assert(contract.load(deploy_address))

    result = contract.register_did(did, ddo, register_account)
    assert(result)
    assert(result == did)

    result = contract.resolve(did, query_address)
    assert(result)
    assert(result == ddo)


    result = contract.owner(did, query_address)
    assert(result)
    assert(result == query_address)

def test_contract_did_register_full_ddo(convex_network, convex_accounts):
    deploy_address = CONTRACT_ACCOUNTS['development']
    register_account = convex_accounts[1]
    auto_topup_account(convex_network, register_account)
    query_address = register_account.address_checksum


    did_id = secrets.token_hex(32)
    did = f'0x{did_id}'
    now = datetime.datetime.now()
    ddo = {
        '@context': 'https://w3id.org/did/v1',
        'id': f'did:dep:{did_id}',
        'created': now.isoformat(sep=' '),
        'service': [
            {
                'type': 'DEP.Invoke.v1',
                'serviceEndpoint': 'http://127.0.0.1:9999/api/v1/invoke'
            },
            {
                'type': 'DEP.Meta.v1',
                'serviceEndpoint': 'http://127.0.0.1:9999/api/v1/meta'
            },
            {
                'type': 'DEP.Storage.v1',
                'serviceEndpoint': 'http://127.0.0.1:9999/api/v1/assets'
            },
            {
                'type': 'DEP.Auth.v1',
                'serviceEndpoint': 'http://127.0.0.1:9999/api/v1/auth'
            }
        ]
    }
    contract = DDORegistryContract(convex_network.convex)
    assert(contract.load(deploy_address))


    result = contract.register_did(did, json.dumps(ddo), register_account)
    assert(result)
    assert(result == did)


    result = contract.resolve(did, query_address)
    assert(result)
    assert(result == json.dumps(ddo))

