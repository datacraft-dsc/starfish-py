"""

    Dex Token Contract

"""
from starfish.network.ethereum.ethereum_account import EthereumAccount
from starfish.types import AccountAddress

from .contract_base import ContractBase


CONTRACT_NAME = 'DatacraftToken'


class DatacraftTokenContract(ContractBase):
    """Class representing the Dex Token contract."""

    def __init__(self) -> None:
        ContractBase.__init__(self, CONTRACT_NAME)

    def get_balance(self, account_address: AccountAddress) -> float:
        address = self.get_account_address(account_address)
        amount_wei = self.call('balanceOf', address)
        return self.to_ether(amount_wei)

    def approve_transfer(self, account: EthereumAccount, to_account_address: AccountAddress, amount: float) -> bool:
        to_address = self.get_account_address(to_account_address)
        amount_wei = self.to_wei(amount)
        return self.call('approve', (to_address, amount_wei), account)

    def transfer(self, account: EthereumAccount, to_account_address: AccountAddress, amount: float) -> bool:
        to_address = self.get_account_address(to_account_address)
        amount_wei = self.to_wei(amount)
        return self.call('transfer', (to_address, amount_wei), account)

    def total_supply(self) -> float:
        amount_wei = self.call('totalSupply')
        return self.to_ether(amount_wei)
