"""

    Command Account Send Token

"""
import logging
from typing import Any

from starfish.network.convex.convex_account import ConvexAccount

from .command_base import CommandBase

logger = logging.getLogger(__name__)


class AccountSendTokenCommand(CommandBase):

    def __init__(self, sub_parser: Any = None) -> None:
        super().__init__('token', sub_parser)

    def create_parser(self, sub_parser: Any):

        parser = sub_parser.add_parser(
            self._name,
            description='Send tokens for an account address',
            help='Send tokens from one account to the another'
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
            help='Address to send data too',
        )

        parser.add_argument(
            'amount',
            help='Amount to send'
        )
        return parser

    def execute(self, args: Any, output: Any) -> None:
        if not self.is_address(args.address):
            output.add_error(f'{args.address} is not a convex account address')
            return

        account = ConvexAccount.import_from_file(args.keyfile, args.password, args.address)
        amount = float(args.amount)
        to_address = args.to_address
        if not self.is_address(to_address):
            output.add_error(f'{to_address} is not a convex address')
            return

        network = self.get_network(args.url)
        logger.debug(f'sending tokens from account {account.address} to account {to_address}')
        network.convex.transfer(to_address, amount, account)

        balance = network.get_balance(account)
        output.add_line(f'Send {amount} tokens from account: {args.address} to account {to_address}')
        output.set_value('balance', balance)
        output.set_value('from_address', args.address)
        output.set_value('to_address', args.to_address)
        output.set_value('amount', amount)
