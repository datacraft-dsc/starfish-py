import pytest


TOKEN_AMOUNT_TO_TRANSFER = 100

def test_ocean_taken_contract(dnetwork, starfish_accounts):

    ocean_token_contract = dnetwork.get_contract('OceanToken')
    dispenser_contract = dnetwork.get_contract('Dispenser')

    from_account = starfish_accounts[0]
    to_account = starfish_accounts[1]

    balance = ocean_token_contract.get_balance(from_account)

    tx_hash = dispenser_contract.request_tokens(TOKEN_AMOUNT_TO_TRANSFER, from_account)
    receipt = dispenser_contract.wait_for_receipt(tx_hash)
    new_balance = ocean_token_contract.get_balance(from_account)
    assert(balance + TOKEN_AMOUNT_TO_TRANSFER == new_balance)

    from_balance = ocean_token_contract.get_balance(from_account)
    to_balance = ocean_token_contract.get_balance(to_account)

    tx_hash = ocean_token_contract.transfer(from_account, to_account.address, TOKEN_AMOUNT_TO_TRANSFER)
    receipt = ocean_token_contract.wait_for_receipt(tx_hash)

    new_from_balance = ocean_token_contract.get_balance(from_account)
    new_to_balance = ocean_token_contract.get_balance(to_account)

    assert(from_balance - TOKEN_AMOUNT_TO_TRANSFER == new_from_balance)
    assert(to_balance + TOKEN_AMOUNT_TO_TRANSFER == new_to_balance)