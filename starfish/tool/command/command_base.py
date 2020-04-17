"""

    Command Base Class

"""

from abc import (
    ABC,
    abstractmethod
)

from starfish import DNetwork

DEFAULT_NETWORK_URL = 'http://localhost:8545'

NETWORK_NAMES = {
    'local': {
        'description': 'Spree network running on a local barge',
        'url': 'http://localhost:8545',
        'faucet_account': ['0x068Ed00cF0441e4829D9784fCBe7b9e26D4BD8d0', 'secret'],
    },
    'spree': {
        'description': 'Spree network running on a local barge',
        'url': 'http://localhost:8545',
        'faucet_account': ['0x068Ed00cF0441e4829D9784fCBe7b9e26D4BD8d0', 'secret'],
    },
    'nile': {
        'description': 'Nile network access to remote network node',
        'url': 'https://nile.dev-ocean.com',
        'faucet_url': 'https://faucet.nile.dev-ocean.com/faucet',
    },
    'pacific': {
        'description': 'Pacific network access to remote network node',
        'url': 'https://pacific.oceanprotocol.com',
        'faucet_url': 'https://faucet.oceanprotocol.com/faucet',
    },
    'duero': {
        'description': 'Duero network access to remote network node',
        'url': 'https://duero.dev-ocean.com',
        'faucet_url': 'https://faucet.duero.dev-ocean.com/faucet',
    },
    'host': {
        'description': 'Local node running on barge',
        'url': 'http://localhost:8545',
    }
}


class CommandBase(ABC):
    def __init__(self, name, sub_parser=None):
        self._name = name
        self._sub_parser = sub_parser
        if sub_parser:
            self.create_parser(sub_parser)

    def is_command(self, name):
        return self._name == name

    def get_network(self, url, default_url=None, load_development_contracts=True):
        if url is None:
            url = default_url
        if url is None:
            url = 'http://localhost:8545'
        network = DNetwork(url, load_development_contracts=load_development_contracts)

        return network

    def get_network_setup(self, name):
        result = None
        if name in NETWORK_NAMES:
            result = NETWORK_NAMES[name]
        return result

    def process_sub_command(self, args, output, command):
        is_found = False
        for command_item in self._command_list:
            if command_item.is_command(command):
                command_item.execute(args, output)
                is_found = True
                break

        if not is_found:
            self.print_help()

    def print_help(self):
        self._sub_parser.choices[self._name].print_help()

    @abstractmethod
    def create_parser(self, sub_parser):
        pass

    @abstractmethod
    def execute(self, args, output):
        pass

    @property
    def name(self):
        return self._name
