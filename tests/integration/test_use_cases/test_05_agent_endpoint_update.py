"""
    test_05_agent_endpoint_update


    As a developer managing a Ocean Agent,
    I need to be able to update service endpoints for my Agent
 
"""

import re

from starfish.agent import SurferAgent
from starfish.ddo.starfish_ddo import StarfishDDO



def test_05_agent_endpoint_update(ocean, config, surfer_agent):
    new_endpoint_uri = '/app/v99/meta/test'
    endpoint = surfer_agent.get_endpoint('metadata')
    assert(endpoint)
    assert(re.search('meta/data', endpoint))

    ddo = SurferAgent.generate_ddo(config.surfer_url)
    ddo.set_service_endpoint('Ocean.Meta.v1', f'{config.surfer_url}{new_endpoint_uri}')
    new_agent = SurferAgent(ocean, ddo=ddo)
    new_endpoint = new_agent.get_endpoint('metadata')
    assert(new_endpoint)
    assert(re.search(new_endpoint_uri, new_endpoint))
