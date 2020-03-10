import pytest

TOKEN_AMOUNT_TO_TRANSFER = 2


def test_dispenser(dnetwork, starfish_accounts):
    dispenser_contract = dnetwork.get_contract('Dispenser')
    ocean_token_contract = dnetwork.get_contract('OceanToken')

    test_account = starfish_accounts[0]
    balance = ocean_token_contract.get_balance(test_account)
    tx_hash = dispenser_contract.request_tokens(TOKEN_AMOUNT_TO_TRANSFER, test_account)
    receipt = dispenser_contract.wait_for_receipt(tx_hash)

    new_balance = ocean_token_contract.get_balance(test_account)
    assert(balance + TOKEN_AMOUNT_TO_TRANSFER == new_balance)
