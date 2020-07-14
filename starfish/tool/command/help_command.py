"""

    Command Help
"""
from typing import Any

from .command_base import CommandBase


class HelpCommand(CommandBase):

    def __init__(self, sub_parser: Any = None, parent_command: Any = None) -> None:
        self._parent_command = parent_command
        super().__init__('help', sub_parser)

    def create_parser(self, sub_parser: Any) -> Any:

        parser = sub_parser.add_parser(
            self._name,
            description='Get help about this command section',
            help='Get more help'

        )
        return parser

    def execute(self, args: Any, output: Any) -> None:
        self._parent_command.print_help()
