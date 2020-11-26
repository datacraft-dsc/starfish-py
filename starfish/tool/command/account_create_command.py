"""

    Tool command Account Create


"""
import logging
from typing import Any

from starfish.network.ethereum.ethereum_account import EthereumAccount
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
        account = EthereumAccount.create(args.password)
        logger.debug(f'create new account {account.address}')
        if args.keyfile:
            logger.debug(f'writing key file to {args.keyfile}')
            account.save_to_file(args.keyfile)
        else:
            logger.debug('writing key file to ouptut')
            output.add_line(account.export_to_text)
        output.add_line(account.address)
        output.set_value('keydata', account.key_data)
        output.set_value('address', account.address)
