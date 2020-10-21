"""

    Test Convex ddo register contract for starfish

"""

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

    ddo_registry_contract = DDORegistryContract(convex_network.convex)
    assert(ddo_registry_contract.load(deploy_address))
    result = ddo_registry_contract.register_did(did, ddo, register_account)
    assert(result)
    assert(result == did)

    result = ddo_registry_contract.resolve(did, query_address)
    assert(result)
    assert(result == ddo)


    result = ddo_registry_contract.owner(did, query_address)
    assert(result)
    assert(result == query_address)
