"""

    Command 'Agent Register'

"""
import re
from typing import Any
from web3 import Web3

from starfish.account import Account
from starfish.agent import RemoteAgent
from starfish.agent.services import (
    ALL_SERVICES,
    Services
)


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
            'address',
            help='register account address to use'
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
Services can be: {",".join(ALL_SERVICES)}
'''
        )
        return parser

    def execute(self, args: Any, output: Any) -> Any:
        network = self.get_network(args.url)

        if not Web3.isAddress(args.address):
            output.add_error(f'{args.address} is not an ethereum account address')
            return

        register_account = Account(args.address, args.password, key_file=args.keyfile)

        all_services = True
        service_list = None
        if args.service_list:
            name_list = re.split(r'[^a-z]+', args.service_list, re.IGNORECASE)
            service_list = []
            print(name_list)
            for name in name_list:
                service_name = name.strip()
                if service_name not in ALL_SERVICES:
                    output.add_error(f'{service_name} is not a valid service')
                    return
                service_list.append(service_name)
            if service_list:
                all_services = False
            else:
                output.add_error(f'No services found to register in list {args.service_list}')
                return

        services = Services(args.agent_url, service_list=service_list, all_services=all_services)
        ddo = RemoteAgent.generate_ddo(services)
        if network.register_did(register_account, ddo.did, ddo.as_text()):
            output.add_line(f'{args.agent_url} has been registered with the did {ddo.did}')
            output.add_line(ddo.as_text())
            output.set_value('did', ddo.did)
            output.set_value('ddo_text', ddo.as_text())
        else:
            output.add_error(f'unable to register {args.agent_url}')
