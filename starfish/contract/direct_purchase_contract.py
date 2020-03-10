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

    def send_token_and_log(self, account, to_account_address, amount, reference1, reference2):
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

        to_address = self.get_account_address(to_account_address)
        amount_wei = self.to_wei(amount)

        tx_hash = self.call(
            'sendTokenAndLog',
            (
                to_address,
                amount_wei,
                self.web3.toBytes(reference1),
                self.web3.toBytes(reference2)
            ),
            account
        )
        return tx_hash

    def check_is_paid(self, from_account_address, to_account_address, amount, reference1=None, reference2=None):
        """
        Check if the log about transaction exists in blockchain.

        :param address_from: Account address sent the tokens from
        :param address_to: Account address, str
        :param amount: token amount, int in unit of Ocean vodka's
        :param reference: reference in log, int256
        :return: bool
        """

        from_address =  self.get_account_address(from_account_address)
        to_address =  self.get_account_address(to_account_address)
        amount_wei = self.to_wei(amount)

        argument_filters = {
            '_from': from_address,
            '_to': to_address,
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
