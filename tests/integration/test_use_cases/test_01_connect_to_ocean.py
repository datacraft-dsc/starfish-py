"""


    test_01_connect_to_ocean


    As a developer working with Ocean,
    I need a way to connect to the Ocean Network

"""

import secrets
import json
from starfish import Ocean
from starfish.agent import RemoteAgent
from starfish.utils.did import did_generate_random


def test_01_connect_to_ocean(ocean, config):
    assert(ocean)


def test_01_connect_to_remote_agent(ocean, config, publisher_account):

    did = did_generate_random()
    assert(did)
    ddo = {
        'name': 'Test ddo',
        'value': secrets.token_hex(64)
    }

    ocean.register_did(did, json.dumps(ddo), publisher_account)
    resolve_ddo = ocean.resolve_did(did)
    assert(resolve_ddo)
    found_ddo = json.loads(resolve_ddo)
    assert(found_ddo == ddo)

def test_01_connect_to_multiple_remote_agent(ocean, config, publisher_account):

    for index in range(0, 2):
        did = did_generate_random()
        assert(did)
        ddo = {
            'name': 'Test ddo',
            'value': secrets.token_hex(64),
            'index': index
        }
        ocean.register_did(did, json.dumps(ddo), publisher_account)
        resolve_ddo = ocean.resolve_did(did)
        assert(resolve_ddo)
        found_ddo = json.loads(resolve_ddo)
        assert(found_ddo == ddo)
