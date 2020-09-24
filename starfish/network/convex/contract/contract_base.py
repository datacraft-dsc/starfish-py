"""


Contract Base

"""


class ContractBase:
    def __init__(self, convex, account, name, version):
        self._convex = convex
        self._account = account
        self._name = name
        self._version = version
        self._source = None
        self._address = None

    def deploy(self):
        if not self._source:
            raise ValueError(f'Cannot deploy the contract {self.name} with no source text')
        deploy_line = f"""
(def {self.name}
    (deploy
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

    def get_address(self):
        address = self._convex.get_address(self._name, self._account)
        return address

    def get_version(self):
        if self._address is None:
            self._address = self.get_address()

        result = self._convex.query(f'(call {self._address} (version))', self._account)
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
