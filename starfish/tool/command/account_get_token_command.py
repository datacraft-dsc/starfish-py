"""

    Command Account Get Token

"""
import logging
from typing import Any


from starfish.network.convex.convex_account import ConvexAccount

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
            nargs='?',
            help='Account keyfile',
        )
        parser.add_argument(
            'keytext',
            nargs='?',
            help='Account keytext',
        )

        parser.add_argument(
            'amount',
            nargs='?',
            default=DEFAULT_AMOUNT,
            help=f'Amount to request. Default {DEFAULT_AMOUNT}'
        )
        return parser

    def execute(self, args: Any, output: Any) -> None:
        if not self.is_address(args.address):
            output.add_error(f'{args.address} is not an convex account address')
            return

        if args.keyfile:
            account = ConvexAccount.import_from_file(args.keyfile, args.password, args.address)
        elif args.keytext:
            account = ConvexAccount.import_from_text(args.keytext, args.password, args.address)
        else:
            output.add_error('no keyfile or key text provided that contains the encrypted account private key')

        network = self.get_network(args.url)
        network.convex.request_funds(int(args.amount), account)

        logger.debug(f'requesting funds for account {account.address}')
        balance = network.convex.get_balance(account)
        output.add_line(f'Get token for account: {args.address} balance: {balance}')
        output.set_value('balance', balance)
        output.set_value('address', args.address)
