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
        address = account_address
        if hasattr(account_address, 'address'):
            address = account_address.address
        amount_wei = self.call('balanceOf', address)
        return self._web3.fromWei(amount_wei, 'ether')

    def approve_tranfer(self, account, to_address, amount):
        amount_wei = self._web3.toWei(amount, 'ether')
        return self.call('approve', (to_address, amount_wei), account)

    def transfer(self, account, to_address, amount):
        amount_wei = self._web3.toWei(amount, 'ether')
        return self.call('transfer', (to_address, amount_wei), account)

    def total_supply(self):
        amount_wei = self.call('totalSupply')
        return self._web3.fromWei(amount_wei, 'ether')
