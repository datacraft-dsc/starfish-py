"""

    Test Convex Network class

"""
import pytest
import secrets

from starfish.utils.did import did_generate_random
from tests.integration.network.convex.helpers import auto_topup_account


TEST_AMOUNT = 5


def test_convex_network_setup(convex_network, config):
    assert(convex_network.url == config['convex']['network']['url'])

def test_convex_network_ddo(convex_network, convex_accounts):
    register_account = convex_accounts[1]
    auto_topup_account(convex_network, register_account)
    did = did_generate_random()
    ddo = f'test - ddo - {did}'

    result = convex_network.register_did(register_account, did, ddo)
    assert(result)
    assert(result == did)

    result = convex_network.resolve_did(did, register_account.address)
    assert(result)
    assert(result == ddo)

def test_convex_network_provenance(convex_network, convex_accounts):
    register_account = convex_accounts[1]
    auto_topup_account(convex_network, register_account)
    asset_id = secrets.token_hex(32)
    result = convex_network.register_provenance(register_account, asset_id)
    print(result)
    assert(result)

    result = convex_network.get_provenance_event_list(asset_id)
    print(result)
    assert(result)
