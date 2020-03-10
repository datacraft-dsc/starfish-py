import pytest


from starfish.utils.did import did_generate_random
from starfish.agent import RemoteAgent
from starfish.agent.services import Services


def test_did_registry_contract(network, config, accounts):
    """

    Register and find a ddo based on a did

    """
    did_registry_contract = network.get_contract('DIDRegistry')

    did = did_generate_random()

    services = Services(config.remote_agent_url, all_services=True)
    ddo = RemoteAgent.generate_ddo(services)
    ddo_text = ddo.as_text()

    register_account = accounts[0]

    tx_hash = did_registry_contract.register(register_account, did, ddo_text)
    receipt = did_registry_contract.wait_for_receipt(tx_hash)

    block_number = did_registry_contract.get_block_number(did)
    assert(receipt.blockNumber == block_number)

    saved_ddo_text = did_registry_contract.get_value(did)
    assert(ddo_text == saved_ddo_text)
