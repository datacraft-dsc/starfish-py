"""
    Helpers for testing

"""


TOPUP_AMOUNT = 10000000

def auto_topup_account(convex_network, account, min_balance=None):
    if isinstance(account, (list, tuple)):
        for account_item in account:
            auto_topup_account(convex_network, account_item, min_balance)
        return
    if min_balance is None:
        min_balance = TOPUP_AMOUNT
    return convex_network.convex.topup_account(account, min_balance)
