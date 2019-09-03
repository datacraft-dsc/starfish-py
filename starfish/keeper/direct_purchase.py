from squid_py.keeper.contract_base import ContractBase
from web3 import Web3
from squid_py.keeper.web3_provider import Web3Provider

class DirectPurchase(ContractBase):
    """Class representing the Token contract."""
    CONTRACT_NAME = 'DirectPurchase'

    def send_token_and_log(self, account, address_to, amount, reference1, reference2):
        """
        Send tokens to address with tracking record in log.

        :param account: The Account to send the tokens from
        :type account: :class:`.Account` object
        :param address_to: Account address, str
        :param amount: token amount, int in unit of Ocean vodka's
        :param reference1: reference in log, int256
        :param reference2: reference in log, int256
        :return: void
        """

        if not Web3Provider.get_web3().isChecksumAddress(address_to):
            address_to = Web3Provider.get_web3().toChecksumAddress(address_to)

        amount = Web3Provider.get_web3().toWei(amount, 'ether')

        tx_hash = self.send_transaction(
            'sendTokenAndLog', (
                address_to,
                amount,
                Web3.toBytes(reference1),
                Web3.toBytes(reference2)
            ),
            transact={
                'from': account.address,
                'passphrase': account.password,
            }
        )
        return self.get_tx_receipt(tx_hash).status == 1
