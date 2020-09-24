"""


Contract Base

"""

from convex_api import Account


class ContractBase:
    def __init__(self, convex, address_account, name, version):
        self._convex = convex
        self._account = address_account
        self._name = name
        self._version = version
        self._source = None
        self._address = None

    def deploy(self):
        if not self._source:
            raise ValueError(f'Cannot deploy the contract {self.name} with no source text')
        if not isinstance(self._account, Account):
            raise TypeError(f'You need to create the contract {self.name} with a valid convex account')

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
        result = self._convex.send(deploy_line, self._account)
        if result and 'value' in result:
            self._address = result['value']
            return self._address

    def load(self):
        self._address = self.get_address()
        self._version = self.get_version()
        return (self._address, self._version)

    def get_address(self):
        address = self._convex.get_address(self._name, self._account)
        return address

    def get_version(self):
        address = self._address
        if address is None:
            address = self.get_address()

        result = self._convex.query(f'(call {address} (version))', self._account)
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
