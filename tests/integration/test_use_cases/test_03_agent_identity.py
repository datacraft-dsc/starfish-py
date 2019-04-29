"""
    test_03_agent_identity


    As a developer working with Ocean,
    I need a stable identifier (Agent ID) for an arbitrary Agent in the Ocean ecosystem
    This test class with validate the DID and DDO format and and their data

"""

import secrets
from starfish.agent import SurferAgent
from starfish.utils.did import did_parse
from starfish.ddo.starfish_ddo import StarfishDDO


def find_surfer_service(service_type):
    for service_name, service in SurferAgent.services.items():
        if service['type'] == service_type:
            return service
    return None

def test_03_agent_did(surfer_agent):
    did = surfer_agent.did
    assert(did)
    data = did_parse(did)
    assert(data)
    assert(data['method'] == 'op')
    assert(data['id_hex'] == '0x' + data['id'])
    assert(data['path'] is None)
    assert(data['fragment'] is None)

def test_03_agent_ddo(surfer_agent):
    ddo = surfer_agent.ddo
    assert(ddo)
    assert(isinstance(ddo, StarfishDDO))
    for service in ddo.services:
        supported_service = find_surfer_service(service.type)
        assert(supported_service)
        endpoint = surfer_agent.get_endpoint(service.type)
        assert(endpoint)
        assert(endpoint == service.endpoints.service)


def test_03_agent_get_endpoints(surfer_agent):
    assert(surfer_agent.get_endpoint('metadata'))
    assert(surfer_agent.get_endpoint('storage'))
    assert(surfer_agent.get_endpoint('invoke'))
    assert(surfer_agent.get_endpoint('market'))
    assert(surfer_agent.get_endpoint('trust'))
    assert(surfer_agent.get_endpoint('auth'))
