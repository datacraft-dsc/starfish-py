"""

    Command Account Get ..

"""

from .account_get_ether_command import AccountGetEtherCommand
from .account_get_token_command import AccountGetTokenCommand
from .command_base import CommandBase

DEFAULT_AMOUNT = 10


class AccountGetCommand(CommandBase):

    def __init__(self, sub_parser=None):
        self._command_list = []
        super().__init__('get', sub_parser)

    def create_parser(self, sub_parser):

        parser = sub_parser.add_parser(
            self._name,
            description='Get ether or tokens for an account address',
            help='Get some token or ether from a faucet or a tokens on a test network'

        )
        get_parser = parser.add_subparsers(
            title='get command',
            description='get command',
            help='Get command',
            dest='get_command'
        )

        self._command_list = [
            AccountGetEtherCommand(get_parser),
            AccountGetTokenCommand(get_parser)
        ]
        return get_parser

    def execute(self, args, output):
        for command_item in self._command_list:
            if command_item.is_command(args.get_command):
                command_item.execute(args, output)
                break
