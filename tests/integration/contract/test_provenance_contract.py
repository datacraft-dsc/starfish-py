import pytest
import secrets
import time

from starfish.utils.did import did_generate_random
from starfish.agent import RemoteAgent
from starfish.agent.services import Services

ASSET_REGISTER_COUNT = 2

def test_provenance_contract(network, accounts):
    """

    Register and find a provenance record on the block chain for a given asset_id

    """
    provenance_contract = network.get_contract('Provenance')

    asset_id = secrets.token_hex(32)

    register_account = accounts[0]

    register_block_number = 0
    for counter in range(0, ASSET_REGISTER_COUNT):
        tx_hash = provenance_contract.register(register_account, asset_id)
        receipt = provenance_contract.wait_for_receipt(tx_hash)
        if register_block_number == 0:
            register_block_number = receipt.blockNumber

    block_number = provenance_contract.get_block_number(asset_id)
    assert(register_block_number == block_number)

    event_list = provenance_contract.get_event_list(asset_id)
    assert(len(event_list) == ASSET_REGISTER_COUNT)
    for event in event_list:
        assert(event['asset_id'] == asset_id)
