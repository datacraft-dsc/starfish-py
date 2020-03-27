"""

Unit test AgentManager

"""
import pytest

from starfish.agent import AgentManager

def test_agent_manager_add(network):
    manager = AgentManager(network)

    authentication = {
        'username': 'user_test',
        'password': 'password_test'
    }
    manager.add('test', 'http://test.com', authentication=authentication)
    assert(manager.items['test'])

    with pytest.raises(ValueError):
        manager.add('failed')
