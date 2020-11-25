import pytest


from starfish.agent import RemoteAgent
from starfish.network.did import did_generate_random
from starfish.network.ddo import DDO

def test_did_registry_contract(ethereum_network, config, ethereum_accounts):
    """

    Register and find a ddo based on a did

    """
    did_registry_contract = ethereum_network.get_contract('DIDRegistry')

    did = did_generate_random()

    local_agent = config['agents']['surfer']
    ddo = DDO.create_for_all_services('http://localhost', did=did)
    ddo_text = ddo.as_text

    register_account = ethereum_accounts[0]

    tx_hash = did_registry_contract.register(register_account, did, ddo_text)
    receipt = did_registry_contract.wait_for_receipt(tx_hash)

    block_number = did_registry_contract.get_block_number(did)
    assert(receipt.blockNumber == block_number)

    saved_ddo_text = did_registry_contract.get_value(did)
    assert(ddo_text == saved_ddo_text)
