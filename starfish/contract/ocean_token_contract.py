"""

    Ocean Token Contract

"""

from .contract_base import ContractBase

CONTRACT_NAME = 'OceanToken'


class OceanTokenContract(ContractBase):
    """Class representing the Ocean Token contract."""

    def __init__(self):
        ContractBase.__init__(self, CONTRACT_NAME)

    def get_balance(self, account_address):
        address = self.get_account_address(account_address)
        amount_wei = self.call('balanceOf', address)
        return self.to_ether(amount_wei)

    def approve_transfer(self, account, to_account_address, amount):
        to_address = self.get_account_address(to_account_address)
        amount_wei = self.to_wei(amount)
        return self.call('approve', (to_address, amount_wei), account)

    def transfer(self, account, to_account_address, amount):
        to_address = self.get_account_address(to_account_address)
        amount_wei = self.to_wei(amount)
        return self.call('transfer', (to_address, amount_wei), account)

    def total_supply(self):
        amount_wei = self.call('totalSupply')
        return self.to_ether(amount_wei)
