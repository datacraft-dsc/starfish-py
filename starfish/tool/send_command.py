"""

    Command 'get_ether'

"""

from .command_base import CommandBase
from .send_ether_command import SendEtherCommand
from .send_token_command import SendTokenCommand

DEFAULT_AMOUNT = 10


class SendCommand(CommandBase):

    def __init__(self, subparser):
        self._command_list = []
        super().__init__('send', subparser)

    def create_parser(self, subparser):

        parser = subparser.add_parser(
            self._name,
            description='Send ether or tokens from one account to another',
            help='Send some tokens or ether from one account to another'
        )

        parser_send = parser.add_subparsers(
            title='send command',
            description='send command',
            help='Send command',
            dest='send_command'
        )

        self._command_list = [
            SendEtherCommand(parser_send),
            SendTokenCommand(parser_send)
        ]

    def execute(self, args, output):
        for command_item in self._command_list:
            if command_item.is_command(args.send_command):
                command_item.execute(args, output)
                break
