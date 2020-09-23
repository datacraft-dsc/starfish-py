"""

    Command Base Class

"""

from abc import (
    ABC,
    abstractmethod
)
from typing import Any

from starfish.network.ethereum.ethereum_network import EthereumNetwork

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
    def __init__(self, name: str, sub_parser: Any = None) -> None:
        self._name = name
        self._sub_parser = sub_parser
        if sub_parser:
            self.create_parser(sub_parser)

    def is_command(self, name: str) -> bool:
        return self._name == name

    def get_network(self, url: str, default_url: str = None, load_development_contracts: bool = True) -> Any:
        if url is None:
            url = default_url
        if url is None:
            url = 'http://localhost:8545'
        network = EthereumNetwork(url, load_development_contracts=load_development_contracts)

        return network

    def get_network_setup(self, name: str) -> Any:
        result = None
        if name in NETWORK_NAMES:
            result = NETWORK_NAMES[name]
        return result

    def process_sub_command(self, args: Any, output: Any, command: str) -> None:
        is_found = False
        for command_item in self._command_list:
            if command_item.is_command(command):
                command_item.execute(args, output)
                is_found = True
                break

        if not is_found:
            self.print_help()

    def print_help(self) -> None:
        self._sub_parser.choices[self._name].print_help()

    @abstractmethod
    def create_parser(self, sub_parser: Any) -> Any:
        pass

    @abstractmethod
    def execute(self, args: Any, output: Any) -> None:
        pass

    @property
    def name(self) -> str:
        return self._name
