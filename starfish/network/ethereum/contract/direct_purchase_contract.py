"""

    Direct Purchase Contract

"""

from starfish.network.ethereum.ethereum_account import EthereumAccount
from starfish.types import AccountAddress

from .contract_base import ContractBase

CONTRACT_NAME = 'DirectPurchase'
TOKEN_SENT_EVENT_NAME = 'TokenSent'


class DirectPurchaseContract(ContractBase):
    """Class representing the Token contract."""

    def __init__(self) -> None:
        ContractBase.__init__(self, CONTRACT_NAME)

    def send_token_and_log(
        self,
        account: EthereumAccount,
        to_account_address: AccountAddress,
        amount: float,
        reference_1: str = None,
        reference_2: str = None
    ) -> str:
        """
        Send tokens to address with tracking record in log.

        :param account: The Account to send the tokens from
        :type account: :class:`.Account` object
        :param address_to: Account address, str
        :param amount: token amount, int in unit of Ocean vodka's
        :param reference1: reference in log, int256
        :param reference2: reference in log, int256
        :return: tx_hash
        """

        if reference_1 is None:
            reference_1 = 0

        if reference_2 is None:
            reference_2 = 0

        to_address = self.get_account_address(to_account_address)
        amount_wei = self.to_wei(amount)

        tx_hash = self.call(
            'sendTokenAndLog',
            (
                to_address,
                amount_wei,
                self.web3.toBytes(hexstr=reference_1),
                self.web3.toBytes(hexstr=reference_2)
            ),
            account
        )
        return tx_hash

    def check_is_paid(
        self,
        from_account_address: AccountAddress,
        to_account_address: AccountAddress,
        amount: float,
        reference_1: str = None,
        reference_2: str = None
    ) -> bool:
        """
        Check if the log about transaction exists in blockchain.

        :param address_from: Account address sent the tokens from
        :param address_to: Account address, str
        :param amount: token amount, int in unit of Ocean vodka's
        :param reference: reference in log, int256
        :return: bool
        """

        from_address = self.get_account_address(from_account_address)
        to_address = self.get_account_address(to_account_address)
        amount_wei = self.to_wei(amount)

        argument_filters = {
            '_from': from_address,
            '_to': to_address,
            '_amount': amount_wei,
        }
        if reference_1:
            argument_filters['_reference1'] = self.web3.toBytes(hexstr=reference_1)

        if reference_2:
            argument_filters['_reference2'] = self.web3.toBytes(hexstr=reference_2)

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
