import pytest

TOKEN_AMOUNT_TO_TRANSFER = 100


def test_dispenser(dnetwork, starfish_accounts):
    dispenser_contract = dnetwork.get_contract('Dispenser')
    ocean_token_contract = dnetwork.get_contract('OceanToken')

    balance = ocean_token_contract.get_balance(starfish_accounts['publisher'])
    tx_hash = dispenser_contract.request_tokens(TOKEN_AMOUNT_TO_TRANSFER, starfish_accounts['publisher'])
    receipt = dispenser_contract.wait_for_receipt(tx_hash)

    new_balance = ocean_token_contract.get_balance(starfish_accounts['publisher'])
    assert(balance + TOKEN_AMOUNT_TO_TRANSFER == new_balance)
