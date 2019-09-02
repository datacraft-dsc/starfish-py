import pytest


from starfish.keeper.direct_purchase import DirectPurchase


def test_direct_purchase(ocean, config, squid_agent):
    adapter = squid_agent.get_adapter
    purchase_contract = DirectPurchase.get_instance()
    account_purchaser = ocean.get_account(config.purchaser_account['address'])
    account_publisher = ocean.get_account(config.publisher_account['address'])
    account_purchaser.set_password(config.purchaser_account['password'])
    account_purchaser.unlock()
    TOKEN_AMOUNT_TO_TRANSFER = 100
    account_purchaser.request_tokens(TOKEN_AMOUNT_TO_TRANSFER)

    balance_purchaser = account_purchaser.ocean_balance_raw
    balance_publisher = account_publisher.ocean_balance_raw

    adapter.approve_tokens(purchase_contract.address, TOKEN_AMOUNT_TO_TRANSFER, account_purchaser)
    account_purchaser.unlock()
    purchase_contract.send_token_and_log(account_purchaser, account_publisher.address, TOKEN_AMOUNT_TO_TRANSFER, 3, 4)

    assert(account_purchaser.ocean_balance_raw + TOKEN_AMOUNT_TO_TRANSFER == balance_purchaser
        and account_publisher.ocean_balance_raw - TOKEN_AMOUNT_TO_TRANSFER == balance_publisher)
