import pytest
import secrets
import time

TOKEN_AMOUNT_TO_TRANSFER = 10


def test_direct_purchase(ethereum_network, ethereum_accounts):
    """

    Transfer funds from the 'buy' account -> 'sell' account

    """
    direct_contract = ethereum_network.get_contract('DirectPurchase')
    datacraft_token_contract = ethereum_network.get_contract('DatacraftToken')
    dispenser_contract = ethereum_network.get_contract('Dispenser')

    from_account = ethereum_accounts[0]
    to_account = ethereum_accounts[1]
    ref_1 = secrets.token_hex(32)
    ref_2 = secrets.token_hex(32)

    tx_hash = dispenser_contract.request_tokens(from_account, TOKEN_AMOUNT_TO_TRANSFER)
    receipt = dispenser_contract.wait_for_receipt(tx_hash)
    # print('request tokens receipt', receipt)
    assert(receipt.status == 1)

    from_balance = datacraft_token_contract.get_balance(from_account)
    to_balance = datacraft_token_contract.get_balance(to_account)

    # datacraft_token_contract.unlockAccount(from_account)

    tx_hash = datacraft_token_contract.approve_transfer(
        from_account,
        direct_contract.address,
        TOKEN_AMOUNT_TO_TRANSFER
    )
    receipt = datacraft_token_contract.wait_for_receipt(tx_hash)
    # print('approve transfer receipt', receipt)
    assert(receipt.status == 1)


    tx_hash = direct_contract.send_token_and_log(
        from_account,
        to_account.address,
        TOKEN_AMOUNT_TO_TRANSFER,
        ref_1,
        ref_2
    )
    receipt = dispenser_contract.wait_for_receipt(tx_hash)
    # print('send token and log receipt', receipt)
    assert(receipt.status == 1)

    new_from_balance = datacraft_token_contract.get_balance(from_account)
    new_to_balance = datacraft_token_contract.get_balance(to_account)

    assert(from_balance - TOKEN_AMOUNT_TO_TRANSFER == new_from_balance)
    assert(to_balance + TOKEN_AMOUNT_TO_TRANSFER == new_to_balance)

    is_sent = direct_contract.check_is_paid(
        from_account.address,
        to_account.address,
        TOKEN_AMOUNT_TO_TRANSFER,
        ref_1
    )
    assert(is_sent)

    is_sent = direct_contract.check_is_paid(
        from_account.address,
        to_account.address,
        TOKEN_AMOUNT_TO_TRANSFER,
        ref_1,
        ref_2
    )
    assert(is_sent)
