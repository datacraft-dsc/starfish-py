"""
    test_06_agent_endpoint_query


    As a developer working with Ocean,
    I need to obtain service endpoints for an arbitrary Agent in the Ocean ecosystem

"""

import re

from starfish.agent import RemoteAgent
from starfish.ddo.starfish_ddo import StarfishDDO


def test_06_agent_endpoint_query(ocean, remote_agent):

    endpoint = remote_agent.get_endpoint('meta')
    assert(re.search('/meta', endpoint))
    endpoint = remote_agent.get_endpoint('storage')
    assert(re.search('/assets', endpoint))
    endpoint = remote_agent.get_endpoint('invoke')
    assert(re.search('/invoke', endpoint))
    endpoint = remote_agent.get_endpoint('market')
    assert(re.search('/market', endpoint))
    endpoint = remote_agent.get_endpoint('trust')
    assert(re.search('/trust', endpoint))
    endpoint = remote_agent.get_endpoint('auth')
    assert(re.search('/auth', endpoint))
