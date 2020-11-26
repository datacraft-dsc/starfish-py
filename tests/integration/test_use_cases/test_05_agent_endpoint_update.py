"""
    test_05_agent_endpoint_update


    As a developer managing a Ocean Agent,
    I need to be able to update service endpoints for my Agent

"""

import pytest
import re

from starfish.agent import RemoteAgent
from starfish.network.ddo import DDO


def test_05_agent_endpoint_update(config, remote_agent_surfer):
    endpoint = remote_agent_surfer.get_endpoint('DEP.Meta.v1')
    assert(endpoint)
    assert(re.search('meta', endpoint))

    local_agent = config['agents']['surfer']
    ddo = DDO.create(local_agent['url'], service_list=['meta'], version='v99')

    new_endpoint_uri = '/app/v99/meta/test'
    new_agent = RemoteAgent(ddo=ddo)
    with pytest.raises(ValueError):
        new_endpoint = new_agent.get_endpoint('DEP.Meta.v99')
