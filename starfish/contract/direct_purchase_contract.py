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

        amount_wei = self.web3.toWei(amount, 'ether')

        tx_hash = self.call(
            'sendTokenAndLog',
            (
                address_to,
                amount_wei,
                self.web3.toBytes(reference1),
                self.web3.toBytes(reference2)
            ),
            account
        )
        return tx_hash

    def check_is_paid(self, address_from, address_to, amount, reference1=None, reference2=None):
        """
        Check if the log about transaction exists in blockchain.

        :param address_from: Account address sent the tokens from
        :param address_to: Account address, str
        :param amount: token amount, int in unit of Ocean vodka's
        :param reference: reference in log, int256
        :return: bool
        """
        amount_wei = self.web3.toWei(amount, 'ether')

        argument_filters = {
            '_from': address_from,
            '_to': address_to,
            '_amount': amount_wei,
        }
        if reference1:
            argument_filters['_reference1'] = self.web3.toBytes(reference1)

        if reference2:
            argument_filters['_reference2'] = self.web3.toBytes(reference2)

        event_filter = self.create_event_filter(
            'TokenSent',
            None,
            from_block=1,
            argument_filters=argument_filters
        )

        if event_filter:
            for event_log in event_filter.get_all_entries():
                event_args = event_log.args
                if event_args._amount == amount_wei:
                    return True

        return False
