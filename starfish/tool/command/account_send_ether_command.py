"""

    Command Account Send Ether

"""
import logging
from typing import Any
from web3 import Web3

from starfish.network.ethereum.ethereum_account import EthereumAccount

from .command_base import CommandBase

logger = logging.getLogger(__name__)


class AccountSendEtherCommand(CommandBase):

    def __init__(self, sub_parser: Any = None) -> None:
        super().__init__('ether', sub_parser)

    def create_parser(self, sub_parser: Any):

        parser = sub_parser.add_parser(
            self._name,
            description='Send ether from an account address to another account',
            help='Send ether from one account to the another'
        )

        parser.add_argument(
            'address',
            help='Account address'
        )

        parser.add_argument(
            'password',
            help='Account password'
        )

        parser.add_argument(
            'keyfile',
            help='Account keyfile'
        )

        parser.add_argument(
            'to_address',
            help='Account address to send data too',
        )

        parser.add_argument(
            'amount',
            help='Amount to send'
        )
        return parser

    def execute(self, args: Any, output: Any) -> None:
        if not Web3.isAddress(args.address):
            output.add_error(f'{args.address} is not an ethereum account address')
            return

        account = EthereumAccount(args.address, args.password, key_file=args.keyfile)
        amount = float(args.amount)
        to_address = args.to_address

        network = self.get_network(args.url)
        logger.debug(f'sending ether from account {account.address} to account {to_address}')
        network.send_ether(account, to_address, amount)

        balance = network.get_token_balance(account)
        output.add_line(f'Send {amount} ether from account: {args.address} to account {to_address}')
        output.set_value('balance', balance)
        output.set_value('from_address', args.address)
        output.set_value('to_address', args.to_address)
        output.set_value('amount', amount)
