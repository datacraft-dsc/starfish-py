import pytest


from starfish.keeper.direct_purchase import DirectPurchase


def test_direct_purchase(ocean, config, squid_agent):
    adapter = squid_agent.get_adapter
    purchase_contract = DirectPurchase.get_instance()
    account_purchaser = ocean.get_account(config.purchaser_account['address'])
    account_publisher = ocean.get_account(config.publisher_account['address'])
    account_purchaser.set_password(config.purchaser_account['password'])
    account_purchaser.unlock()
    account_purchaser.request_tokens(50)

    adapter.approve_tokens(purchase_contract.address, 50, account_purchaser)
