"""

    Command Account Get ..

"""
from typing import Any

from .account_get_ether_command import AccountGetEtherCommand
from .account_get_token_command import AccountGetTokenCommand
from .command_base import CommandBase
from .help_command import HelpCommand

DEFAULT_AMOUNT = 10


class AccountGetCommand(CommandBase):

    def __init__(self, sub_parser: Any = None) -> None:
        self._command_list = []
        super().__init__('get', sub_parser)

    def create_parser(self, sub_parser: Any) -> Any:

        parser = sub_parser.add_parser(
            self._name,
            description='Get ether or tokens for an account address',
            help='Get some token or ether from a faucet or a tokens on a test network'

        )
        account_get_parser = parser.add_subparsers(
            title='get command',
            description='get command',
            help='Get command',
            dest='get_command'
        )

        self._command_list = [
            AccountGetEtherCommand(account_get_parser),
            AccountGetTokenCommand(account_get_parser),
            HelpCommand(account_get_parser, self)
        ]
        return account_get_parser

    def execute(self, args: Any, output: Any) -> Any:
        return self.process_sub_command(args, output, args.get_command)
