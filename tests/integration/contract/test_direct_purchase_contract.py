import pytest


from starfish.contract import DirectPurchaseContract, DispenserContract
from starfish.contract import ContractManager

TOKEN_AMOUNT_TO_TRANSFER = 100
REFERENCE_1 = 4
REFERENCE_2 = 5

def test_direct_purchase(config, publisher_account, purchaser_account):
    manager = ContractManager(config.keeper_url)
    direct_contract = manager.load('direct_purchase_contract')

    dispenser_contract = manager.load('dispenser_contract')

    dispenser_contract.request_tokens(TOKEN_AMOUNT_TO_TRANSFER, purchaser_account)

    purchaser_balance = purchaser_account.ocean_balance
    publisher_balance = publisher_account.ocean_balance

    direct_contract.send_token_and_log(purchaser_account, publisher_account.address, TOKEN_AMOUNT_TO_TRANSFER, REFERENCE_1, REFERENCE_2)

    assert(purchaser_account.ocean_balance + TOKEN_AMOUNT_TO_TRANSFER == purchaser_balance
        and publisher_account.ocean_balance - TOKEN_AMOUNT_TO_TRANSFER == publisher_balance)

def test_is_paid(config, publisher_account, purchaser_account):
    manager = ContractManager(config.keeper_url)
    direct_contract = manager.load('direct_purchase_contract')
    isPaid = direct_contract.check_is_paid(purchaser_account.address, publisher_account.address, TOKEN_AMOUNT_TO_TRANSFER, REFERENCE_2)
    assert(isPaid)
