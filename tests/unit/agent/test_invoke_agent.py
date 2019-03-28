
import pytest
import secrets


from starfish.agent.invoke_agent import InvokeAgent

TEST_KOI_URL = 'http:testkoi.com:8080'


def test_init(ocean):
    agent = InvokeAgent()
    assert(agent)
    
    agent = InvokeAgent(koi_url=TEST_KOI_URL)
    assert(agent)

def test_get_operations():
    # this class is not ready yet for 
    # unit testing 'requests'
    """
    agent = InvokeAgent(koi_url=TEST_KOI_URL)
    operations = agent.get_operations()
    assert(operations)
    """
