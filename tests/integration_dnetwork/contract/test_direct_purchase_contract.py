import pytest


TOKEN_AMOUNT_TO_TRANSFER = 100
REFERENCE_1 = 4
REFERENCE_2 = 5


def test_direct_purchase(dnetwork, starfish_accounts):
    """

    Transfer funds from the 'buy' account -> 'sell' account

    """
    direct_contract = dnetwork.get_contract('DirectPurchase')
    ocean_token_contract = dnetwork.get_contract('OceanToken')
    dispenser_contract = dnetwork.get_contract('Dispenser')


    from_account = starfish_accounts[0]
    to_account = starfish_accounts[1]


    tx_hash = dispenser_contract.request_tokens(TOKEN_AMOUNT_TO_TRANSFER, from_account)
    receipt = dispenser_contract.wait_for_receipt(tx_hash)
    # print('request tokens receipt', receipt)
    assert(receipt.status == 1)

    from_balance = ocean_token_contract.get_balance(from_account)
    to_balance = ocean_token_contract.get_balance(to_account)

    # ocean_token_contract.unlockAccount(from_account)

    tx_hash = ocean_token_contract.approve_tranfer(
        from_account,
        direct_contract.address,
        TOKEN_AMOUNT_TO_TRANSFER
    )
    receipt = ocean_token_contract.wait_for_receipt(tx_hash)
    # print('approve transfer receipt', receipt)
    assert(receipt.status == 1)


    tx_hash = direct_contract.send_token_and_log(
        from_account,
        to_account.address,
        TOKEN_AMOUNT_TO_TRANSFER,
        REFERENCE_1,
        REFERENCE_2
    )
    receipt = dispenser_contract.wait_for_receipt(tx_hash)
    # print('send token and log receipt', receipt)
    assert(receipt.status == 1)

    new_from_balance = ocean_token_contract.get_balance(from_account)
    new_to_balance = ocean_token_contract.get_balance(to_account)

    print('from', from_balance, new_from_balance)
    print('to', to_balance, new_to_balance)

    assert(from_balance - TOKEN_AMOUNT_TO_TRANSFER == new_from_balance)
    assert(to_balance + TOKEN_AMOUNT_TO_TRANSFER == new_to_balance)

def test_is_paid(dnetwork, starfish_accounts):
    direct_contract = dnetwork.get_contract('DirectPurchase')
    from_account = starfish_accounts[0]
    to_account = starfish_accounts[1]

    isPaid = direct_contract.check_is_paid(
        from_account.address,
        to_account.address,
        TOKEN_AMOUNT_TO_TRANSFER,
        REFERENCE_1
    )
    assert(isPaid)
