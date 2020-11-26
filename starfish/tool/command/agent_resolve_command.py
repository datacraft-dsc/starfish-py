"""

    Command 'Agent Resolve'

"""
from typing import Any

from .command_base import CommandBase


class AgentResolveCommand(CommandBase):

    def __init__(self, sub_parser: Any = None) -> None:
        self._command_list = []
        super().__init__('resolve', sub_parser)

    def create_parser(self, sub_parser: Any) -> Any:

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

    def execute(self, args: Any, output: Any) -> None:
        network = self.get_network(args.url)

        output.set_value('agent', args.agent)

        ddo = network.resolve_agent(args.agent, username=args.username, password=args.password)
        if ddo:
            output.add_line(f'{args.agent} resolved to {ddo.as_text}')
            output.add_line(f'did: {ddo.did}')
            output.set_value('ddo_text', ddo.as_text)
            output.set_value('did', ddo.did)
        else:
            output.add_line(f'unable to resolve agent address {args.agent}')
