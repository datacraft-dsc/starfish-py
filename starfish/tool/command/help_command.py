"""

    Command Help
"""

from .command_base import CommandBase


class HelpCommand(CommandBase):

    def __init__(self, sub_parser=None, parent_command=None):
        self._parent_command = parent_command
        super().__init__('help', sub_parser)

    def create_parser(self, sub_parser):

        parser = sub_parser.add_parser(
            self._name,
            description='Get help about this command section',
            help='Get more help'

        )
        return parser

    def execute(self, args, output):
        self._parent_command.print_help()
