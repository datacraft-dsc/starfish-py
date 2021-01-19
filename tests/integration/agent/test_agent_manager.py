"""

Unit test AgentManager

"""
import pytest
import secrets

from starfish.agent_manager import AgentManager
from starfish.asset import DataAsset
from starfish.network.ddo import DDO


def test_agent_manager_register(config, ethereum_network):
    manager = AgentManager()

    manager.register_agents(config['agents'])

    assert(manager.items)

def test_agent_manager_load_agent(config, ethereum_network):
    manager = AgentManager()

    agent_items = config['agents']
    manager.register_agents(agent_items)

    name = 'surfer'
    assert(name == 'surfer')
    ddo = manager.load_ddo(name)
    assert(ddo)
    # load a named item
    remote_agent = manager.load_agent(name)
    assert(remote_agent)
    assert(remote_agent.did == ddo.did)

    # load from a agent did
    remote_agent = manager.load_agent(ddo.did)
    assert(remote_agent)
    assert(remote_agent.did == ddo.did)


    test_data = secrets.token_hex(1024)
    asset_data = DataAsset.create('TestAsset', test_data)
    asset = remote_agent.register_asset(asset_data)
    assert(asset)

    # load from a asset_did
    remote_agent = manager.load_agent(asset.did)
    assert(remote_agent)
    assert(remote_agent.did == ddo.did)

