"""

    Command 'Agent Resolve'

"""

from starfish.agent import AgentManager
from .command_base import CommandBase


class AgentResolveCommand(CommandBase):

    def __init__(self, sub_parser=None):
        self._command_list = []
        super().__init__('resolve', sub_parser)

    def create_parser(self, sub_parser):

        parser = sub_parser.add_parser(
            self._name,
            description='Tool to resolve an agent',
            help='Tool to resolve an agent using its DID or URL',

        )

        parser.add_argument(
            '-u',
            '--username',
            help='Username to access the remote agent'
        )

        parser.add_argument(
            '-p',
            '--password',
            help='Password to access the remote agent'
        )

        parser.add_argument(
            'agent',
            help='agent url or agent did to resolve. If url, you may need to provide --username and --password options'
        )

        return parser

    def execute(self, args, output):
        network = self.get_network(args.url)

        output.set_value('agent', args.agent)

        result = AgentManager.resolve_agent(args.agent, network, args.username, args.password)
        if result:
            output.add_line(f'{args.agent} resolved to {result["ddo_text"]}')
            for name, value in result.items():
                output.set_value(name, value)
        else:
            output.add_line(f'unable to resolve agent address {args.agent}')
