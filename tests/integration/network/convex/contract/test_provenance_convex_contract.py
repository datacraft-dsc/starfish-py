"""

    Test Convex ddo register contract for starfish

"""
from eth_utils import add_0x_prefix
import pytest
import secrets
from tests.integration.network.convex.helpers import auto_topup_account

from convex_api.account import Account
from convex_api.convex_api import ConvexAPI
from convex_api.exceptions import ConvexAPIError

from starfish.network.convex.contract.provenance_contract import ProvenanceContract

# (import convex.trust :as trust)


def test_contract_provenance_methods(convex_network, convex_accounts):

    TEST_COUNT = 4
    register_account = convex_accounts[1]
    auto_topup_account(convex_network, register_account)
    query_address = register_account.address

    did = f'0x{secrets.token_hex(32)}'
    ddo = f'test - ddo - {did}'

    contract = ProvenanceContract(convex_network.convex)
    assert(contract)
    assert(contract.address)
    register_asset_id_list = []
    for index in range(0, TEST_COUNT):
        asset_id = f'0x{secrets.token_hex(32)}'
        register_asset_id_list.append(asset_id)
        result = contract.register(asset_id, register_account)
        assert(result)
        assert(result['asset_id'] == asset_id)
        assert(result['owner'] == query_address)


    for asset_id in register_asset_id_list:
        result = contract.event_list(asset_id, query_address)
        print(result)
        assert(result)
        assert(result[0]['asset_id'] == asset_id)
        assert(result[0]['owner'] == query_address)

    result = contract.event_owner(query_address)
    assert(result)
    assert(len(result) == len(register_asset_id_list))
