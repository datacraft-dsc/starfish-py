"""


    test_01_connect_to_ocean


    As a developer working with Ocean,
    I need a way to connect to the Ocean Network

"""

import secrets
import json
from starfish import DNetwork
from starfish.agent import RemoteAgent
from starfish.utils.did import did_generate_random


def test_01_connect_to_network(network, config):
    assert(network)


def test_01_connect_to_remote_agent(network, config, accounts):

    register_account = accounts[0]
    did = did_generate_random()
    assert(did)
    ddo = {
        'name': 'Test ddo',
        'value': secrets.token_hex(64)
    }

    network.register_did(register_account, did, json.dumps(ddo))
    resolve_ddo = network.resolve_did(did)
    assert(resolve_ddo)
    found_ddo = json.loads(resolve_ddo)
    assert(found_ddo == ddo)

def test_01_connect_to_multiple_remote_agent(network, config, accounts):

    register_account = accounts[0]
    for index in range(0, 2):
        did = did_generate_random()
        assert(did)
        ddo = {
            'name': 'Test ddo',
            'value': secrets.token_hex(64),
            'index': index
        }
        network.register_did(register_account, did, json.dumps(ddo))
        resolve_ddo = network.resolve_did(did)
        assert(resolve_ddo)
        found_ddo = json.loads(resolve_ddo)
        assert(found_ddo == ddo)
