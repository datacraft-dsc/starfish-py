import pytest


from starfish.contract import ContractManager

TOKEN_AMOUNT_TO_TRANSFER = 100

def test_ocean_taken_contract(config, starfish_accounts):
    manager = ContractManager(config.keeper_url)

    ocean_token_contract = manager.load('ocean_token_contract')
    dispenser_contract = manager.load('dispenser_contract')

    balance = ocean_token_contract.get_balance(starfish_accounts['publisher'])

    tx_hash = dispenser_contract.request_tokens(TOKEN_AMOUNT_TO_TRANSFER, starfish_accounts['publisher'])
    receipt = dispenser_contract.wait_for_receipt(tx_hash)
    new_balance = ocean_token_contract.get_balance(starfish_accounts['publisher'])
    assert(balance + TOKEN_AMOUNT_TO_TRANSFER == new_balance)
