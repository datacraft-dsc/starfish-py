"""


    test_01_connect_to_network


    As a developer working with a network,
    I need a way to connect to the network

"""

import secrets
import json
from starfish.agent import RemoteAgent
from starfish.utils.did import did_generate_random


def test_01_connect_to_network(ethereum_network, config):
    assert(ethereum_network)


def test_01_connect_to_remote_agent(ethereum_network, config, ethereum_accounts):

    register_account = ethereum_accounts[0]
    did = did_generate_random()
    assert(did)
    ddo = {
        'name': 'Test ddo',
        'value': secrets.token_hex(64)
    }

    ethereum_network.register_did(register_account, did, json.dumps(ddo))
    resolve_ddo = ethereum_network.resolve_did(did)
    assert(resolve_ddo)
    found_ddo = json.loads(resolve_ddo)
    assert(found_ddo == ddo)

def test_01_connect_to_multiple_remote_agent(ethereum_network, config, ethereum_accounts):

    register_account = ethereum_accounts[0]
    for index in range(0, 2):
        did = did_generate_random()
        assert(did)
        ddo = {
            'name': 'Test ddo',
            'value': secrets.token_hex(64),
            'index': index
        }
        ethereum_network.register_did(register_account, did, json.dumps(ddo))
        resolve_ddo = ethereum_network.resolve_did(did)
        assert(resolve_ddo)
        found_ddo = json.loads(resolve_ddo)
        assert(found_ddo == ddo)
