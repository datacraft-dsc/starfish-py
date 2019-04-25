"""
    test_05_agent_endpoint_update

"""

from starfish.agent import SurferAgent
from starfish.ddo.starfish_ddo import StarfishDDO



def test_05_agent_endpoint_update(surfer_agent):
    new_endpoint_uri = '/app/v99/meta/test',
    endpoint = surfer_agent.get_endpoint('metadata')
    assert(endpoint)
