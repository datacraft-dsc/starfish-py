"""

    Network class to provide basic functionality for convex network

"""
from convex_api import ConvexAPI

from starfish.network.account_base import AccountBase
from starfish.network.network_base import NetworkBase


class ConvexNetwork(NetworkBase):
    def __init__(self, url: str) -> None:
        NetworkBase.__init__(self, url)
        self._convex = ConvexAPI(url)

    """

    Register DID with a DDO and resolve DID to a DDO

    """
    def register_did(self, account: AccountBase, did: str, ddo_text: str) -> bool:
        return False

    def resolve_did(self, did: str) -> str:
        return None

    @property
    def convex(self):
        return self._convex
