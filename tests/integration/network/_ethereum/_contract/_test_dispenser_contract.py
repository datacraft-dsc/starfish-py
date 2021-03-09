import pytest

TOKEN_AMOUNT_TO_TRANSFER = 2


def test_dispenser(ethereum_network, ethereum_accounts):
    dispenser_contract = ethereum_network.get_contract('Dispenser')
    datacraft_token_contract = ethereum_network.get_contract('DatacraftToken')

    test_account = ethereum_accounts[0]
    balance = datacraft_token_contract.get_balance(test_account)
    tx_hash = dispenser_contract.request_tokens(test_account, TOKEN_AMOUNT_TO_TRANSFER)
    receipt = dispenser_contract.wait_for_receipt(tx_hash)

    new_balance = datacraft_token_contract.get_balance(test_account)
    assert(balance + TOKEN_AMOUNT_TO_TRANSFER == new_balance)
