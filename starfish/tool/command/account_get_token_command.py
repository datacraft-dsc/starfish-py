"""

    Command Account Get Token

"""
import logging
from typing import Any
from web3 import Web3

from starfish.account import Account

from .command_base import CommandBase

logger = logging.getLogger(__name__)


DEFAULT_AMOUNT = 10


class AccountGetTokenCommand(CommandBase):

    def __init__(self, sub_parser: Any = None) -> None:
        super().__init__('token', sub_parser)

    def create_parser(self, subparser: Any) -> Any:

        parser = subparser.add_parser(
            self._name,
            description='Get tokens for an account address',
            help='Get some token from the development network'
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
            'amount',
            nargs='?',
            default=DEFAULT_AMOUNT,
            help=f'Amount to request. Default {DEFAULT_AMOUNT}'
        )
        return parser

    def execute(self, args: Any, output: Any) -> None:
        if not Web3.isAddress(args.address):
            output.add_error(f'{args.address} is not an ethereum account address')
            return

        account = Account(args.address, args.password, key_file=args.keyfile)

        network = self.get_network(args.url)
        network.request_test_tokens(account, int(args.amount))

        logger.debug(f'requesting tokens for account {account.address}')
        balance = network.get_token_balance(account)
        output.add_line(f'Get {args.get_command} for account: {args.address} balance: {balance}')
        output.set_value('balance', balance)
        output.set_value('address', args.address)
