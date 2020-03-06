import pytest


from starfish.contract import ContractManager
from starfish.utils.did import did_generate_random
from starfish.agent import RemoteAgent
from starfish.agent.services import Services


def test_did_registry_contract(config, starfish_accounts):
    """

    Register and find a ddo based on a did

    """
    manager = ContractManager(config.keeper_url)
    did_registry_contract = manager.load('DIDRegistryContract', abi_filename='DIDRegistry.development.json')

    did = did_generate_random()

    services = Services(config.remote_agent_url, all_services=True)
    ddo = RemoteAgent.generate_ddo(services)
    ddo_text = ddo.as_text()

    register_account = starfish_accounts['purchaser']

    tx_hash = did_registry_contract.register(register_account, did, ddo_text)
    receipt = did_registry_contract.wait_for_receipt(tx_hash)

    block_number = did_registry_contract.get_block_number_for_did(did)
    assert(receipt.blockNumber == block_number)

    saved_ddo_text = did_registry_contract.get_value(did)
    assert(ddo_text == saved_ddo_text)
