"""

    Account class to provide basic functionality for convex network

"""

from starfish.network.account_base import AccountBase
from convex_api import Account as ConvexAPIAccount

class ConvexAccount(ConvexAPIAccount, AccountBase):
    pass
