"""

    Test RemoteAgent Unit


"""
import requests

from starfish.agent.remote_agent import RemoteAgent
from starfish.middleware.agent.remote_agent_adapter import RemoteAgentAdapter
from starfish.network.ddo import DDO


def test_remote_agent_set_http_client():
    ddo = DDO.create('http://localhost:3030')
    agent = RemoteAgent(ddo)
    assert(agent.http_client)
    new_client = object()
    agent.http_client = new_client
    assert(agent.http_client)
    assert(isinstance(agent.http_client, object))


def test_remote_agent_get_adapter():
    ddo = DDO.create('http://localhost:3030')
    agent = RemoteAgent(ddo)
    assert(agent.adapter)
    assert(isinstance(agent.adapter, RemoteAgentAdapter))
