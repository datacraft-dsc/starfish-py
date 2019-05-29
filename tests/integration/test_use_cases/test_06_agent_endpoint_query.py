"""
    test_06_agent_endpoint_query


    As a developer working with Ocean,
    I need to obtain service endpoints for an arbitrary Agent in the Ocean ecosystem

"""

import re

from starfish.agent import SurferAgent
from starfish.ddo.starfish_ddo import StarfishDDO


def test_06_agent_endpoint_query(ocean, surfer_agent):

    endpoint = surfer_agent.get_endpoint('metadata')
    assert(re.search('/meta/data', endpoint))
    endpoint = surfer_agent.get_endpoint('storage')
    assert(re.search('/assets', endpoint))
    endpoint = surfer_agent.get_endpoint('invoke')
    assert(re.search('/api/v1$', endpoint))
    endpoint = surfer_agent.get_endpoint('market')
    assert(re.search('/market$', endpoint))
    endpoint = surfer_agent.get_endpoint('trust')
    assert(re.search('/trust$', endpoint))
    endpoint = surfer_agent.get_endpoint('auth')
    assert(re.search('/auth$', endpoint))
