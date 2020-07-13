"""

    Command Account Send ..

"""
from typing import Any

from .account_send_ether_command import AccountSendEtherCommand
from .account_send_token_command import AccountSendTokenCommand
from .command_base import CommandBase
from .help_command import HelpCommand

DEFAULT_AMOUNT = 10


class AccountSendCommand(CommandBase):

    def __init__(self, sub_parser: Any = None) -> None:
        self._command_list = []
        super().__init__('send', sub_parser)

    def create_parser(self, sub_parser: Any) -> Any:

        parser = sub_parser.add_parser(
            self._name,
            description='Send ether or tokens from one account to another',
            help='Send some tokens or ether from one account to another'
        )

        account_send_parser = parser.add_subparsers(
            title='send command',
            description='send command',
            help='Send command',
            dest='send_command'
        )

        self._command_list = [
            AccountSendEtherCommand(account_send_parser),
            AccountSendTokenCommand(account_send_parser),
            HelpCommand(account_send_parser, self)
        ]
        return account_send_parser

    def execute(self, args: Any, output: Any) -> Any:
        return self.process_sub_command(args, output, args.send_command)
