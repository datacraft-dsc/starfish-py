"""

    Command 'Agent'

"""
from typing import Any

from .agent_register_command import AgentRegisterCommand
from .agent_resolve_command import AgentResolveCommand
from .command_base import CommandBase
from .help_command import HelpCommand


class AgentCommand(CommandBase):

    def __init__(self, sub_parser: Any = None) -> None:
        self._command_list = []
        super().__init__('agent', sub_parser)

    def create_parser(self, sub_parser: Any) -> Any:

        parser = sub_parser.add_parser(
            self._name,
            description='Tool tasks for agents',
            help='Tasks to perform on agents',

        )
        agent_parser = parser.add_subparsers(
            title='Agent sub command',
            description='Agent sub command',
            help='Agent sub command',
            dest='agent_command'
        )

        self._command_list = [
            AgentRegisterCommand(agent_parser),
            AgentResolveCommand(agent_parser),
            HelpCommand(agent_parser, self)
        ]
        return agent_parser

    def execute(self, args: Any, output: Any) -> Any:
        return self.process_sub_command(args, output, args.agent_command)
