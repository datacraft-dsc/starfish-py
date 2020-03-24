"""
    test_04_agent_registration


    As a developer building or managing an Ocean Agent,
    I need to be able to register my Agent on the network and obtain an Agent ID

"""

from starfish.agent import RemoteAgent
from starfish.ddo import DDO



def test_04_agent_register_and_resolve(network, config, accounts):

    remote_agent = config.agent_list['remote']
    ddo = RemoteAgent.generate_ddo(remote_agent['url'])
    options = {
        'username': remote_agent['username'],
        'password': remote_agent['password']
    }

    register_account = accounts[0]

    did = ddo.did
    assert(network.register_did(register_account, did, ddo.as_text()))
    found_ddo = DDO(json_text=network.resolve_did(did))
    assert(found_ddo.as_text() == ddo.as_text())

    resolved_agent = RemoteAgent(network, ddo)
    assert(resolved_agent)
    assert(resolved_agent.ddo)
    assert(resolved_agent.ddo.as_text() == ddo.as_text())
