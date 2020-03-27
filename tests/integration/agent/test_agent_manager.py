"""

Unit test AgentManager

"""
import pytest
import secrets

from starfish.agent import AgentManager
from starfish.asset import DataAsset


def test_agent_manager_add(config, network):
    manager = AgentManager(network)

    for name, item in config.agent_list.items():
        manager.add(name, item)

    assert(manager.items)
    for name, item in manager.items.items():
        assert(config.agent_list[name])


    for name, item in config.agent_list.items():
        ddo = manager.resolve_ddo(name)
        assert(ddo)

def test_agent_manager_load_agent(config, network):
    manager = AgentManager(network)

    for name, item in config.agent_list.items():
        manager.add(name, item)

    items = config.agent_list;
    name = manager.default_name
    assert(name == 'remote')
    ddo_text = manager.resolve_ddo(name)
    ddo = AgentManager.create_ddo_object(ddo_text)

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

