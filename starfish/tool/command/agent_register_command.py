"""

    Command 'Agent Register'

"""
import re
from typing import Any

from starfish.agent.remote_agent import SUPPORTED_SERVICES
from starfish.network.ddo import DDO
from starfish.network.ethereum.ethereum_account import EthereumAccount


from .command_base import CommandBase


class AgentRegisterCommand(CommandBase):

    def __init__(self, sub_parser: Any = None) -> None:
        self._command_list = []
        super().__init__('register', sub_parser)

    def create_parser(self, sub_parser: Any) -> Any:

        parser = sub_parser.add_parser(
            self._name,
            description='Tool to register an agent',
            help='Tool to register an agent on the network',

        )

        parser.add_argument(
            'agent_url',
            help='url of the agent to register, you may need to provide --username and --password options'
        )

        parser.add_argument(
            'password',
            help='account password to use to register'
        )

        parser.add_argument(
            'keyfile',
            help='account key_file use to register'
        )

        parser.add_argument(
            'service_list',
            nargs='?',
            help=f'''
Optional list of services, if not given then all services will be registed.
Services can be: {",".join(SUPPORTED_SERVICES)}
'''
        )
        return parser

    def execute(self, args: Any, output: Any) -> Any:
        network = self.get_network(args.url)

        register_account = EthereumAccount.import_from_file(args.keyfile, args.password)

        service_list = None
        if args.service_list:
            name_list = re.split(r'[^a-z]+', args.service_list, re.IGNORECASE)
            service_list = []
            for name in name_list:
                service_name = name.strip()
                if service_name not in SUPPORTED_SERVICES:
                    output.add_error(f'{service_name} is not a valid service')
                    return
                service_list.append(service_name)

        ddo = DDO.create(args.agent_url, service_list=service_list)
        if network.register_did(register_account, ddo.did, ddo.as_text):
            output.add_line(f'{args.agent_url} has been registered with the did {ddo.did}')
            output.add_line(ddo.as_text)
            output.set_value('did', ddo.did)
            output.set_value('ddo_text', ddo.as_text)
        else:
            output.add_error(f'unable to register {args.agent_url}')
