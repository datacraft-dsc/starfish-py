"""
    test_04_agent_registration


    As a developer building or managing an Ocean Agent,
    I need to be able to register my Agent on the network and obtain an Agent ID

"""

from starfish.agent import RemoteAgent
from starfish.ddo import DDO



def test_04_agent_register_and_resolve(ethereum_network, config, ethereum_accounts):

    local_agent = config['agents']['local']
    ddo = RemoteAgent.generate_ddo(local_agent['url'])
    authentication = {
        'username': local_agent['username'],
        'password': local_agent['password']
    }

    register_account = ethereum_accounts[0]

    did = ddo.did
    remote_agent = RemoteAgent.register(ethereum_network, register_account, ddo, authentication)
    assert(remote_agent)
    found_ddo = DDO(json_text=ethereum_network.resolve_did(did))
    assert(found_ddo.as_text() == ddo.as_text())


    resolved_agent = RemoteAgent.load(ddo.did, ethereum_network, authentication=authentication)
    assert(resolved_agent)
    assert(resolved_agent.ddo)
    assert(resolved_agent.ddo.as_text() == ddo.as_text())
