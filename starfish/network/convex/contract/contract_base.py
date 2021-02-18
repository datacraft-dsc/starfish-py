"""


Contract Base

"""

from convex_api import ConvexAPI

from starfish.network.convex.contract.convex_registry import ConvexRegistry


class ContractBase:
    def __init__(self, convex: ConvexAPI, name: str):
        self._convex = convex
        self._name = name
        self._registry = ConvexRegistry(convex)
        self._version = None
        self._address = None
        self._owner_address = None

    def send(self, transaction, account):
        if not self.address:
            raise ValueError(f'No contract address found for {self._name}')
        return self._convex.send(f'(call {self.address} {transaction})', account)

    def query(self, transaction, account_address=None):
        if account_address is None:
            account_address = self.address
        if not self.address:
            raise ValueError(f'No contract address found for {self._name}')
        return self._convex.query(f'(call {self.address} {transaction})', account_address)

    @property
    def deploy_version(self):
        if self.address:
            result = self.query('(version)')
            if result and 'value' in result:
                return result['value']

    @property
    def is_registered(self):
        return self.address is not None

    @property
    def address(self):
        if self._address is None:
            self._address = self._registry.resolve_address(self._name)
        return self._address

    @property
    def owner_address(self):
        if self._owner_address is None:
            self._owner_address = self._registry.resolve_owner(self._name)
        return self._owner_address

    @property
    def name(self):
        return self._name

    @property
    def version(self):
        return self._version
