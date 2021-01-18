"""

Unit test AgentManager

"""
import pytest

from starfish.agent_manager import AgentManager
from starfish.network.ddo import DDO

def test_agent_manager_add():
    manager = AgentManager()

    authentication = {
        'username': 'user_test',
        'password': 'password_test'
    }
    ddo = DDO.create('http://test.com')
    manager.register_local_agent(ddo, authentication=authentication)
    assert(manager.local_agent)

    with pytest.raises(ValueError):
        manager.register_local_agent('failed')
