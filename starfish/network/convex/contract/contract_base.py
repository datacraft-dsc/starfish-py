"""


Contract Base

"""

from starfish.network.convex.convex_account import ConvexAccount
from starfish.network.convex.convex_network import ConvexNetwork


class ContractBase:
    def __init__(self, convex: ConvexNetwork, name: str, version: str):
        self._convex = convex
        self._name = name
        self._version = version
        self._source = None
        self._address = None

    def deploy(self, account: ConvexAccount):
        if not self._source:
            raise ValueError(f'Cannot deploy the contract {self.name} with no source text')

        deploy_line = f"""
(def {self.name}
    (deploy-once
        (quote
            (do
                {self._source}
            )
        )
    )
)"""
        result = self._convex.send(deploy_line, account)
        if result and 'value' in result:
            self._address = result['value']
            return self._address

    def load(self, deploy_account: str):
        self._address = self.get_address(deploy_account)
        self._version = self.get_version(deploy_account)
        return (self._address, self._version)

    def get_address(self, deploy_account):
        address = self._convex.get_address(self._name, deploy_account)
        return address

    def get_version(self, deploy_account):
        address = self._address
        if address is None:
            address = self.get_address(deploy_account)

        result = self._convex.query(f'(call {address} (version))', deploy_account)
        if result and 'value' in result:
            return result['value']

    @property
    def name(self):
        return self._name

    @property
    def version(self):
        return self._version

    @property
    def address(self):
        return self._address
