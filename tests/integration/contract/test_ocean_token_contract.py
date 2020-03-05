import pytest


from starfish.contract import ContractManager

TOKEN_AMOUNT_TO_TRANSFER = 100

def test_ocean_taken_contract(config, starfish_accounts):
    manager = ContractManager(config.keeper_url)

    ocean_token_contract = manager.load('OceanTokenContract')
    dispenser_contract = manager.load('DispenserContract')

    balance = ocean_token_contract.get_balance(starfish_accounts['purchaser'])

    tx_hash = dispenser_contract.request_tokens(TOKEN_AMOUNT_TO_TRANSFER, starfish_accounts['purchaser'])
    receipt = dispenser_contract.wait_for_receipt(tx_hash)
    new_balance = ocean_token_contract.get_balance(starfish_accounts['purchaser'])
    assert(balance + TOKEN_AMOUNT_TO_TRANSFER == new_balance)


    from_account = starfish_accounts['purchaser']
    to_account = starfish_accounts['publisher']

    from_balance = ocean_token_contract.get_balance(from_account)
    to_balance = ocean_token_contract.get_balance(to_account)

    tx_hash = ocean_token_contract.transfer(from_account, to_account.address, TOKEN_AMOUNT_TO_TRANSFER)
    receipt = ocean_token_contract.wait_for_receipt(tx_hash)

    new_from_balance = ocean_token_contract.get_balance(from_account)
    new_to_balance = ocean_token_contract.get_balance(to_account)

    assert(from_balance - TOKEN_AMOUNT_TO_TRANSFER == new_from_balance)
    assert(to_balance + TOKEN_AMOUNT_TO_TRANSFER == new_to_balance)