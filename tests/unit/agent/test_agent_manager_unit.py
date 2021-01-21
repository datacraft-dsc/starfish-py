"""

Unit test AgentManager

"""
import pytest
import requests

from starfish.agent_manager import AgentManager
from starfish.network.ddo import DDO

def test_agent_manager_register_agent():
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

def test_agent_manager_find_agent_access():
    manager = AgentManager()

    ddo = DDO.create('http://test.com')
    manager.register_agent('test_agent', ddo=ddo)

    access = manager.find_agent_access('test_agent')

    assert(access)
    assert(access.ddo.as_text == ddo.as_text)

    access = manager.find_agent_access('invalid_test_agent')

    assert(not access)

def test_agent_manager_unregister_agent():
    manager = AgentManager()

    ddo = DDO.create('http://test.com')
    manager.register_agent('test_agent', ddo=ddo)
    access = manager.find_agent_access('test_agent')

    assert(access)
    assert(access.ddo.as_text == ddo.as_text)

    manager.unregister_agent('test_agent')
    access = manager.find_agent_access('test_agent')

    assert(not access)

def test_agent_manager_load_ddo():
    manager = AgentManager()

    ddo = DDO.create('http://test.com')
    manager.register_agent('test_agent', ddo_text=ddo.as_text)
    result_ddo = manager.load_ddo('test_agent')
    assert(result_ddo)
    assert(result_ddo.as_text == ddo.as_text)

def test_agent_manager_is_agent():

    manager = AgentManager()

    ddo = DDO.create('http://test.com')
    manager.register_agent('test_agent', ddo=ddo)

    assert(manager.is_agent('test_agent'))
    assert(not manager.is_agent('invalid_test_agent'))


def test_agent_manager_resolve_with_no_network():
    manager = AgentManager()

    url = 'http://invalid_agent.org'
    with pytest.raises(requests.exceptions.ConnectionError):
        result = manager.resolve_agent_url(url)
