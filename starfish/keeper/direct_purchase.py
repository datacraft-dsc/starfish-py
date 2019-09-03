from squid_py.keeper.contract_base import ContractBase
from squid_py.keeper.web3_provider import Web3Provider
from squid_py.keeper.event_listener import EventListener

class DirectPurchase(ContractBase):
    """Class representing the Token contract."""
    CONTRACT_NAME = 'DirectPurchase'
    TOKEN_SENT_EVENT_NAME = 'TokenSent'

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
                Web3Provider.get_web3().toBytes(reference1),
                Web3Provider.get_web3().toBytes(reference2)
            ),
            transact={
                'from': account.address,
                'passphrase': account.password,
            }
        )
        return self.get_tx_receipt(tx_hash).status == 1

    def check_is_paid(self, address_from, address_to, amount, reference):
        """
        Check if the log about transaction exists in blockchain.

        :param address_from: Account address sent the tokens from
        :param address_to: Account address, str
        :param amount: token amount, int in unit of Ocean vodka's
        :param reference: reference in log, int256
        :return: bool
        """
        reference = Web3Provider.get_web3().toBytes(reference)
        events = EventListener(
            self.CONTRACT_NAME,
            self.TOKEN_SENT_EVENT_NAME,
            None,
            filters={'_from': address_from, '_to': address_to, '_reference2': reference},
            from_block=1, # TODO: later can be optimized
            to_block='latest'
        )

        event = events.event_filter.get_all_entries()

        for key in event:
            event_args = key.args
            if event_args._amount == amount:
                return True
        return False

