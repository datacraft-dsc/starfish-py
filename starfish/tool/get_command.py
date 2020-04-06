"""

    Command 'get_ether'

"""

from .command_base import CommandBase
from .get_ether_command import GetEtherCommand
from .get_token_command import GetTokenCommand

DEFAULT_AMOUNT = 10


class GetCommand(CommandBase):

    def __init__(self, subparser):
        self._command_list = []
        super().__init__('get', subparser)

    def create_parser(self, subparser):

        parser = subparser.add_parser(
            self._name,
            description='Get ether or tokens for an account address',
            help='Get some token or ether from a faucet or a tokens on a test network'

        )
        parser_get = parser.add_subparsers(
            title='get command',
            description='get command',
            help='Get command',
            dest='get_command'
        )

        self._command_list = [
            GetEtherCommand(parser_get),
            GetTokenCommand(parser_get)
        ]

    def execute(self, args, output):
        for command_item in self._command_list:
            if command_item.is_command(args.get_command):
                command_item.execute(args, output)
                break
