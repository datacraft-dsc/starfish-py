"""

    Direct Purchase Contract

"""

from web3 import Web3
from .contract_base import ContractBase

CONTRACT_NAME = 'Dispenser'

class DispenserContract(ContractBase):
    """Class representing the Token contract."""

    def __init__(self):
        ContractBase.__init__(self, CONTRACT_NAME)


    def request_tokens(self, amount, account):
        wei_amount = Web3.toWei(amount, 'ether')
        return self.call('requestTokens', wei_amount, account)



