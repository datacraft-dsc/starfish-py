"""
    test_04_agent_registration


    As a developer building or managing an Ocean Agent,
    I need to be able to register my Agent on the network and obtain an Agent ID

"""

from starfish.agent import SurferAgent
from starfish.ddo.starfish_ddo import StarfishDDO



def test_04_agent_register_and_resolve(ocean, config):

    ddo = SurferAgent.generate_ddo(config.surfer_url)
    options = {
        'url': config.surfer_url,
        'username': config.surfer_username,
        'password': config.surfer_password
    }

    register_account = ocean.get_account(config.publisher_account)
    register_account.unlock()

    did = ddo.did
    assert(ocean.register_did(ddo.did, ddo.as_text(), register_account))
    found_ddo = StarfishDDO(json_text=ocean.resolve_did(did))
    assert(found_ddo.as_text() == ddo.as_text())

    resolved_agent = SurferAgent(ocean, did=did)
    assert(resolved_agent)
    assert(resolved_agent.ddo)
    assert(resolved_agent.ddo.as_text() == ddo.as_text())