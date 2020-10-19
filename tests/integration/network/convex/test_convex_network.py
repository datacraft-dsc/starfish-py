"""

    Test Convex Network class

"""
import pytest
import secrets

from tests.integration.network.convex.helpers import auto_topup_account


TEST_AMOUNT = 5


def test_convex_network_setup(convex_network, config):
    assert(convex_network.url == config['convex']['network']['url'])

def test_convex_network_ddo(convex_network, convex_accounts):
    register_account = convex_accounts[1]
    auto_topup_account(convex_network, register_account)
    did = f'0x{secrets.token_hex(32)}'
    ddo = f'test - ddo - {did}'

    result = convex_network.register_did(did, ddo, register_account)
    assert(result)
    assert(result == did)

    result = convex_network.resolve_did(did, register_account.address)
    assert(result)
    assert(result == ddo)
