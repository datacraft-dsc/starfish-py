"""

    Network class to provide basic functionality for convex network

"""
from convex_api import ConvexAPI

from starfish.network.convex.convex_account import ConvexAccount
from starfish.network.network_base import NetworkBase
from starfish.types import AccountAddress

DEFAULT_PACKAGE_NAME = 'starfish.network.convex.contract'


class ConvexNetwork(NetworkBase):
    def __init__(self, url: str) -> None:
        NetworkBase.__init__(self, url)
        self._convex = ConvexAPI(url)
        from starfish.network.convex.contract.contract_manager import ContractManager
        self._manager = ContractManager(self._convex, DEFAULT_PACKAGE_NAME)

    """

    Register DID with a DDO and resolve DID to a DDO

    """
    def register_did(self, did: str, ddo_text: str, account: ConvexAccount) -> bool:
        ddo_registry_contract = self._manager.load('DDORegistryContract')
        if ddo_registry_contract:
            return ddo_registry_contract.register_did(did, ddo_text, account)

    def resolve_did(self, did: str, account_address: AccountAddress) -> str:
        ddo_registry_contract = self._manager.load('DDORegistryContract')
        if ddo_registry_contract:
            return ddo_registry_contract.resolve(did,  account_address)
        return None

    @property
    def convex(self):
        return self._convex
