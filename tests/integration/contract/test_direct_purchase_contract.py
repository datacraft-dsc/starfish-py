import pytest


from starfish.contract import ContractManager

TOKEN_AMOUNT_TO_TRANSFER = 100
REFERENCE_1 = 4
REFERENCE_2 = 5

def test_direct_purchase(config, starfish_accounts):
    """

    Transfer funds from the 'buy' account -> 'sell' account

    """
    manager = ContractManager(config.keeper_url)
    direct_contract = manager.load('DirectPurchaseContract')
    ocean_token_contract = manager.load('OceanTokenContract')
    dispenser_contract = manager.load('DispenserContract')

    from_account = starfish_accounts['purchaser']
    to_account = starfish_accounts['publisher']
    dispenser_contract.request_tokens(TOKEN_AMOUNT_TO_TRANSFER, from_account)

    from_balance = ocean_token_contract.get_balance(from_account)
    to_balance = ocean_token_contract.get_balance(to_account)

    tx_hash = ocean_token_contract.approve_tranfer(
        from_account,
        to_account.address,
        TOKEN_AMOUNT_TO_TRANSFER
    )
    receipt = ocean_token_contract.wait_for_receipt(tx_hash)
    print('approve transfer receipt', receipt)


    tx_hash = direct_contract.send_token_and_log(
        from_account,
        to_account.address,
        TOKEN_AMOUNT_TO_TRANSFER,
        REFERENCE_1,
        REFERENCE_2
    )
    receipt = dispenser_contract.wait_for_receipt(tx_hash)
    print('send token and log receipt', receipt)

    new_from_balance = ocean_token_contract.get_balance(from_account)
    new_to_balance = ocean_token_contract.get_balance(to_account)

    print('from', from_balance, new_from_balance)
    print('to', to_balance, new_to_balance)

    assert(from_balance - TOKEN_AMOUNT_TO_TRANSFER == new_from_balance)
    assert(to_balance + TOKEN_AMOUNT_TO_TRANSFER == new_to_balance)

def test_is_paid(config, starfish_accounts):
    manager = ContractManager(config.keeper_url)
    direct_contract = manager.load('DirectPurchaseContract')
    buy_account = starfish_accounts['purchaser']
    sell_account = starfish_accounts['publisher']

    isPaid = direct_contract.check_is_paid(
        buy_account.address,
        sell_account.address,
        TOKEN_AMOUNT_TO_TRANSFER,
        REFERENCE_2
    )
    assert(isPaid)
