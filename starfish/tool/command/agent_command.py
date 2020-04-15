"""

    Command 'Agent'

"""

from .agent_register_command import AgentRegisterCommand
from .agent_resolve_command import AgentResolveCommand
from .command_base import CommandBase


class AgentCommand(CommandBase):

    def __init__(self, sub_parser=None):
        self._command_list = []
        super().__init__('agent', sub_parser)

    def create_parser(self, sub_parser):

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
            AgentResolveCommand(agent_parser)
        ]
        return agent_parser

    def execute(self, args, output):
        for command_item in self._command_list:
            if command_item.is_command(args.agent_command):
                command_item.execute(args, output)
                break
