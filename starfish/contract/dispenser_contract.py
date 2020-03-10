"""

    Direct Purchase Contract

"""

from .contract_base import ContractBase

CONTRACT_NAME = 'Dispenser'


class DispenserContract(ContractBase):
    """Class representing the Ocean token dispenser contract."""

    def __init__(self):
        ContractBase.__init__(self, CONTRACT_NAME)

    def request_tokens(self, account, amount):
        # amount is in ether
        return self.call('requestTokens', amount, account)
