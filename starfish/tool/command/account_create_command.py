"""

    Tool command Account Create


"""
import logging
import os
from typing import Any

from starfish.network.convex.convex_account import ConvexAccount
from .command_base import CommandBase

logger = logging.getLogger(__name__)


class AccountCreateCommand(CommandBase):

    def __init__(self, sub_parser: Any = None) -> None:
        super().__init__('create', sub_parser)

    def create_parser(self, sub_parser):
        parser = sub_parser.add_parser(
            self._name,
            description='Create a new account',
            help='Create a new account'

        )
        parser.add_argument(
            'password',
            help='Password of new account'
        )

        parser.add_argument(
            'keyfile',
            nargs='?',
            help='Optional name of the keyfile to write the account key data to'
        )
        return parser

    def execute(self, args: Any, output: Any) -> None:
        network = self.get_network(args.url)
        base_account = None
        if args.password and args.keyfile:
            base_account = ConvexAccount.import_from_file(args.keyfile, args.password)
        account = network.create_account(base_account)
        logger.debug(f'create new account {account.address}')
        if args.keyfile and not os.path.exists(args.keyfile):
            logger.debug(f'writing key file to {args.keyfile}')
            account.export_to_file(args.keyfile, args.password)
        else:
            logger.debug('writing key file to ouptut')
            output.add_line(account.export_to_text(args.password))
        output.add_line(account.address)
        output.set_value('public_key', account.public_key)
        output.set_value('export_key', account.export_to_text(args.password))
        output.set_value('address', account.address)
