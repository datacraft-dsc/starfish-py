"""
    test_03_agent_identity


    As a developer working with Ocean,
    I need a stable identifier (Agent ID) for an arbitrary Agent in the Ocean ecosystem
    This test class with validate the DID and DDO format and and their data

"""

import secrets
from starfish.agent import RemoteAgent
from starfish.utils.did import did_parse
from starfish.ddo.starfish_ddo import StarfishDDO


def find_remote_service(find_service_type):
    for service_name, service_type in RemoteAgent.service_types.items():
        if service_type == find_service_type:
            return service_type
    return None

def test_03_agent_did(remote_agent):
    did = remote_agent.did
    assert(did)
    data = did_parse(did)
    assert(data)
    assert(data['method'] == 'dep')
    assert(data['id_hex'] == '0x' + data['id'])
    assert(data['path'] is None)
    assert(data['fragment'] is None)

def test_03_agent_ddo(remote_agent):
    ddo = remote_agent.ddo
    assert(ddo)
    assert(isinstance(ddo, StarfishDDO))
    for service in ddo.services:
        service_type = find_remote_service(service.type)
        assert(service_type)
        endpoint = remote_agent.get_endpoint(service_type)
        assert(endpoint)
        assert(endpoint == service.endpoints.service)


def test_03_agent_get_endpoints(remote_agent):
    assert(remote_agent.get_endpoint('meta'))
    assert(remote_agent.get_endpoint('storage'))
    assert(remote_agent.get_endpoint('invoke'))
    assert(remote_agent.get_endpoint('market'))
    assert(remote_agent.get_endpoint('trust'))
    assert(remote_agent.get_endpoint('auth'))
