"""

    Command 'Network'

"""

from .command_base import CommandBase
from .help_command import HelpCommand
from .network_wait_command import NetworkWaitCommand


class NetworkCommand(CommandBase):

    def __init__(self, sub_parser=None):
        self._command_list = []
        super().__init__('network', sub_parser)

    def create_parser(self, sub_parser):

        parser = sub_parser.add_parser(
            self._name,
            description='Tool tasks on network',
            help='Tasks to perform on the network',

        )
        network_parser = parser.add_subparsers(
            title='Network sub command',
            description='Network sub command',
            help='Network sub command',
            dest='network_command'
        )

        self._command_list = [
            NetworkWaitCommand(network_parser),
            HelpCommand(network_parser, self)
        ]
        return network_parser

    def execute(self, args, output):
        return self.process_sub_command(args, output, args.network_command)
