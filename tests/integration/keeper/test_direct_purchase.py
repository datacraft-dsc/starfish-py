import pytest


from starfish.keeper.direct_purchase import DirectPurchase

TOKEN_AMOUNT_TO_TRANSFER = 100
REFERENCE_1 = 4
REFERENCE_2 = 5

def test_direct_purchase(ocean, config, squid_agent):
    adapter = squid_agent.get_adapter
    purchase_contract = DirectPurchase.get_instance()
    account_purchaser = ocean.get_account(config.purchaser_account['address'])
    account_publisher = ocean.get_account(config.publisher_account['address'])
    account_purchaser.set_password(config.purchaser_account['password'])
    account_purchaser.unlock()

    account_purchaser.request_tokens(TOKEN_AMOUNT_TO_TRANSFER)

    balance_purchaser = account_purchaser.ocean_balance
    balance_publisher = account_publisher.ocean_balance

    adapter.approve_tokens(purchase_contract.address, TOKEN_AMOUNT_TO_TRANSFER, account_purchaser)
    purchase_contract.send_token_and_log(account_purchaser, account_publisher.address, TOKEN_AMOUNT_TO_TRANSFER, REFERENCE_1, REFERENCE_2)

    assert(account_purchaser.ocean_balance + TOKEN_AMOUNT_TO_TRANSFER == balance_purchaser
        and account_publisher.ocean_balance - TOKEN_AMOUNT_TO_TRANSFER == balance_publisher)

def test_is_paid(ocean, config):
    purchase_contract = DirectPurchase.get_instance()
    account_purchaser = ocean.get_account(config.purchaser_account['address'])
    account_publisher = ocean.get_account(config.publisher_account['address'])
    isPaid = purchase_contract.check_is_paid(account_purchaser.address, account_publisher.address, TOKEN_AMOUNT_TO_TRANSFER, REFERENCE_2)
    assert(isPaid)