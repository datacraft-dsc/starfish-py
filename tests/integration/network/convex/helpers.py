"""
    Helpers for testing

"""




def auto_topup_account(convex_network, account, min_balance=None):
    if isinstance(account, (list, tuple)):
        for account_item in account:
            auto_topup_account(convex_network, account_item, min_balance)
        return
    amount = 1000000
    retry_counter = 100
    if min_balance is None:
        min_balance = amount
    balance = convex_network.convex.get_balance(account)
    while balance < min_balance and retry_counter > 0:
        request_amount = convex_network.convex.request_funds(amount, account)
        balance = convex_network.convex.get_balance(account)
        retry_counter -= 1
