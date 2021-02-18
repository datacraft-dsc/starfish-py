"""

    Test Convex did contract for starfish

"""

import datetime
import json
import pytest
import secrets
from tests.integration.network.convex.helpers import auto_topup_account

from convex_api.account import Account
from convex_api.convex_api import ConvexAPI
from convex_api.exceptions import ConvexAPIError

from starfish.network.convex.contract.did_contract import DIDContract
from starfish.network.did import did_generate_random

# (import convex.trust :as trust)


def test_contract_did_methods(convex_network, convex_accounts):

    register_account = convex_accounts[1]
    auto_topup_account(convex_network, register_account)
    query_address = register_account.address

    did = did_generate_random()
    ddo = f'test - ddo - {did}'

    contract = DIDContract(convex_network.convex)
    assert(contract)
    assert(contract.address)

    result = contract.register_did(did, ddo, register_account)
    assert(result)
    assert(result == did)

    result = contract.resolve(did, query_address)
    assert(result)
    assert(result == ddo)


    result = contract.owner(did, query_address)
    assert(result)
    assert(result == query_address)

def test_contract_did_full_ddo(convex_network, convex_accounts):
    register_account = convex_accounts[1]
    auto_topup_account(convex_network, register_account)
    query_address = register_account.address

    did = did_generate_random()

    now = datetime.datetime.now()
    ddo = {
        '@context': 'https://w3id.org/did/v1',
        'id': did,
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
    contract = DIDContract(convex_network.convex)
    assert(contract)
    assert(contract.address)

    result = contract.register_did(did, json.dumps(ddo), register_account)
    assert(result)
    assert(result == did)


    result = contract.resolve(did, query_address)
    assert(result)
    assert(result == json.dumps(ddo))


def test_contract_did_long_string(convex_network, convex_accounts):
    big_data = '''
{
    "activity": {
        "21bac5c9": {
            "dep:inputs": {
                "$": "{\"date_from\": \"2020-01-01\", \"user_id\": \"7HZQ9P\"}",
                "type": "xsd:string"
            },
            "prov:type": {
                "$": "dep:invoke",
                "type": "xsd:string"
            }
        }
    },
    "agent": {
        "did:dep:118d107119d8d293f7b25701730545abe9db8e5c633a995b295166c32e97dccc": {
            "prov:type": {
                "$": "dep:service-provider",
                "type": "xsd:string"
            }
        }
    },
    "entity": {
        "dep:this": {
            "prov:type": {
                "$": "dep:asset",
                "type": "xsd:string"
            }
        },
        "did:dep:118d107119d8d293f7b25701730545abe9db8e5c633a995b295166c32e97dccc/4d96cd618a3971424c048d417cc759cdaebd0da3d465f94feb5d2f25796ce739": {
            "prov:type": {
                "$": "dep:asset",
                "type": "xsd:string"
            }
        }
    },
    "prefix": {
        "dep": "http://datacraft.sg",
        "prov": "http://www.w3.org/ns/prov#",
        "xsd": "http://www.w3.org/2001/XMLSchema#"
    },
    "wasAssociatedWith": {
        "_:assoc_1": {
            "prov:activity": "21bac5c9",
            "prov:agent": "did:dep:118d107119d8d293f7b25701730545abe9db8e5c633a995b295166c32e97dccc"
        }
    },
    "wasDerivedFrom": {
        "_:derived_1": {
            "prov:generatedEntity": "dep:this",
            "prov:usedEntity": "did:dep:118d107119d8d293f7b25701730545abe9db8e5c633a995b295166c32e97dccc/4d96cd618a3971424c048d417cc759cdaebd0da3d465f94feb5d2f25796ce739"
        }
    },
    "wasGeneratedBy": {
        "_:gen_1": {
            "prov:activity": "21bac5c9",
            "prov:entity": "dep:this"
        }
    }
}
'''

    register_account = convex_accounts[1]
    query_address = register_account.address

    auto_topup_account(convex_network, register_account)
    did = did_generate_random()


    contract = DIDContract(convex_network.convex)
    assert(contract)
    assert(contract.address)

    result = contract.register_did(did, big_data, register_account)
    assert(result)
    assert(result == did)

    result = contract.resolve(did, query_address)
    assert(result)
    assert(result == big_data)
