"""
    test_05_agent_endpoint_update


    As a developer managing a Ocean Agent,
    I need to be able to update service endpoints for my Agent

"""

import pytest
import re

from starfish.agent import RemoteAgent
from starfish.ddo.starfish_ddo import StarfishDDO
from starfish.agent.services import Services, ALL_SERVICES



def test_05_agent_endpoint_update(ocean, config, remote_agent):
    endpoint = remote_agent.get_endpoint('DEP.Meta.v1')
    assert(endpoint)
    assert(re.search('meta', endpoint))

    services = Services(config.remote_agent_url, ['meta'], 'v99')

    ddo = RemoteAgent.generate_ddo(services)
    new_endpoint_uri = '/app/v99/meta/test'
    new_agent = RemoteAgent(ocean, ddo=ddo)
    with pytest.raises(ValueError):
        new_endpoint = new_agent.get_endpoint('DEP.Meta.v99')
