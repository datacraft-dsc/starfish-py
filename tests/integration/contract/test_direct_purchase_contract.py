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
    direct_contract = manager.load('direct_purchase_contract')
    ocean_token_contract = manager.load('ocean_token_contract')
    dispenser_contract = manager.load('dispenser_contract')

    buy_account = starfish_accounts['purchaser']
    sell_account = starfish_accounts['publisher']
    dispenser_contract.request_tokens(TOKEN_AMOUNT_TO_TRANSFER, buy_account)

    buy_balance = ocean_token_contract.get_balance(buy_account)
    sell_balance = ocean_token_contract.get_balance(sell_account)

    tx_hash = ocean_token_contract.approve_tranfer(
        buy_account,
        sell_account.address,
        TOKEN_AMOUNT_TO_TRANSFER
    )
    receipt = ocean_token_contract.wait_for_receipt(tx_hash)

    tx_hash = direct_contract.send_token_and_log(
        buy_account,
        sell_account.address,
        TOKEN_AMOUNT_TO_TRANSFER,
        REFERENCE_1,
        REFERENCE_2
    )
    receipt = dispenser_contract.wait_for_receipt(tx_hash)

    new_buy_balance = ocean_token_contract.get_balance(buy_account)
    new_sell_balance = ocean_token_contract.get_balance(sell_account)

    print('buy', buy_balance, new_buy_balance)
    print('sell', sell_balance, new_sell_balance)

#    assert(sell_balance + TOKEN_AMOUNT_TO_TRANSFER == new_sell_balance
#        and buy_balance - TOKEN_AMOUNT_TO_TRANSFER == new_buy_balance)

def test_is_paid(config, starfish_accounts):
    manager = ContractManager(config.keeper_url)
    direct_contract = manager.load('direct_purchase_contract')
    buy_account = starfish_accounts['purchaser']
    sell_account = starfish_accounts['publisher']

    isPaid = direct_contract.check_is_paid(
        buy_account.address,
        sell_account.address,
        TOKEN_AMOUNT_TO_TRANSFER,
        REFERENCE_2
    )
    assert(isPaid)
