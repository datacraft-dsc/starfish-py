import pytest


from starfish.contract import DispenserContract
from starfish.contract import ContractManager

TOKEN_AMOUNT_TO_TRANSFER = 100


def test_dispenser(config, starfish_accounts):
    manager = ContractManager(config.keeper_url)

    dispenser_contract = manager.load('dispenser_contract')

    tx_hash = dispenser_contract.request_tokens(TOKEN_AMOUNT_TO_TRANSFER, starfish_accounts['publisher'])

    print(tx_hash)
    receipt = dispenser_contract.wait_for_receipt(tx_hash)
