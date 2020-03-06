"""

    DIDRegistry Contract

"""

from .contract_base import ContractBase

CONTRACT_NAME = 'DIDRegistry'


class DIDRegistryContract(ContractBase):
    """

    Class representing the DIDRegistry contract.

    """

    def __init__(self):
        ContractBase.__init__(self, CONTRACT_NAME)


    def register(self, account, did, ddo):
        tx_hash = self.call('registerAttribute', (did_id, ddo), account)
        return tx_hash