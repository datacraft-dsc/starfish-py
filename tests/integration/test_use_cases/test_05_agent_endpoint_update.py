"""
    test_05_agent_endpoint_update


    As a developer managing a Ocean Agent,
    I need to be able to update service endpoints for my Agent

"""

import re

from starfish.agent import RemoteAgent
from starfish.ddo.starfish_ddo import StarfishDDO



def test_05_agent_endpoint_update(ocean, config, remote_agent):
    new_endpoint_uri = '/app/v99/meta/test'
    endpoint = remote_agent.get_endpoint('metadata')
    assert(endpoint)
    assert(re.search('meta/data', endpoint))

    ddo = RemoteAgent.generate_ddo(config.remote_agent_url)
    ddo.set_service_endpoint('Ocean.Meta.v1', f'{config.remote_agent_url}{new_endpoint_uri}')
    new_agent = RemoteAgent(ocean, ddo=ddo)
    new_endpoint = new_agent.get_endpoint('metadata')
    assert(new_endpoint)
    assert(re.search(new_endpoint_uri, new_endpoint))
