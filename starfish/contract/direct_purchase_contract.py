"""

    Direct Purchase Contract

"""

from .contract_base import ContractBase


CONTRACT_NAME = 'DirectPurchase'
TOKEN_SENT_EVENT_NAME = 'TokenSent'

class DirectPurchaseContract(ContractBase):
    """Class representing the Token contract."""

    def __init__(self):
        ContractBase.__init__(self, CONTRACT_NAME)

    def request_tokens(self, amount):
        return 0

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

        if not self.web3.isChecksumAddress(address_to):
            address_to = self.web3.toChecksumAddress(address_to)

        account.approve_tokens(self.address, amount)

        amount = self.web3.toWei(amount, 'ether')

        transaction_hash = self.call(
            'sendTokenAndLog',
            (
                address_to,
                amount,
                self.web3.toBytes(reference1),
                self.web3.toBytes(reference2)
            ),
            account
        )

        print(transaction_hash)
        """
        tx_hash = self.send_transaction(
            'sendTokenAndLog', (
                address_to,
                amount,
                self.w3.toBytes(reference1),
                self.w3.toBytes(reference2)
            ),
            transact={
                'from': account.address,
                'passphrase': account.password,
                'keyfile': account.key_file
            }
        )
        """
        return self.get_tx_receipt(transaction_hash).status == 1

    def check_is_paid(self, address_from, address_to, amount, reference):
        """
        Check if the log about transaction exists in blockchain.

        :param address_from: Account address sent the tokens from
        :param address_to: Account address, str
        :param amount: token amount, int in unit of Ocean vodka's
        :param reference: reference in log, int256
        :return: bool
        """
        reference = self.web3.toBytes(reference)
        amount = self.web3.toWei(amount, 'ether')

        filter = self.web3.eth.filter(
            {
                # '_from': address_from,
                # '_to': address_to,
                # '_reference2': reference,
                'fromBlock': 1,
                'toBlock': 'latest'
            }
        )
        print(self.web3.eth.getFilterChanges(filter.filter_id))
        return True