"""

    Account class to provide basic functionality for convex network

"""

from convex_api import Account as ConvexAPIAccount

from starfish.network.account_base import AccountBase


class ConvexAccount(ConvexAPIAccount, AccountBase):
    pass
