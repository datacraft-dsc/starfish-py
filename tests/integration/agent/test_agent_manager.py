"""

Unit test AgentManager

"""
import pytest

from starfish.agent import AgentManager

def test_agent_manager_add(config, network):
    manager = AgentManager(network)

    for name, item in config.agent_list.items():
        manager.add(name, item)

    assert(manager.items)
    for name, item in manager.items.items():
        assert(config.agent_list[name])


    for name, item in config.agent_list.items():
        ddo = manager.get_ddo(name)
        assert(ddo)