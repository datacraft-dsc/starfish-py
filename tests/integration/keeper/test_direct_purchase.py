import pytest


from starfish.keeper.direct_purchase import DirectPurchase

TOKEN_AMOUNT_TO_TRANSFER = 100
REFERENCE_1 = 4
REFERENCE_2 = 5

def test_direct_purchase(ocean, config, squid_agent, publisher_account, purchaser_account):
    purchaser_contract = DirectPurchase.get_instance()

    purchaser_account.request_tokens(TOKEN_AMOUNT_TO_TRANSFER)

    purchaser_balance = purchaser_account.ocean_balance
    publisher_balance = publisher_account.ocean_balance

    purchaser_contract.send_token_and_log(purchaser_account, publisher_account.address, TOKEN_AMOUNT_TO_TRANSFER, REFERENCE_1, REFERENCE_2)

    assert(purchaser_account.ocean_balance + TOKEN_AMOUNT_TO_TRANSFER == purchaser_balance
        and publisher_account.ocean_balance - TOKEN_AMOUNT_TO_TRANSFER == publisher_balance)

def test_is_paid(ocean, config, publisher_account, purchaser_account):
    purchaser_contract = DirectPurchase.get_instance()
    isPaid = purchaser_contract.check_is_paid(purchaser_account.address, publisher_account.address, TOKEN_AMOUNT_TO_TRANSFER, REFERENCE_2)
    assert(isPaid)
