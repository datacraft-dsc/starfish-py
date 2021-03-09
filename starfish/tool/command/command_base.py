"""

    Command Base Class

"""

from abc import (
    ABC,
    abstractmethod
)
from typing import Any

from convex_api.utils import is_address

from starfish.network.convex.convex_network import ConvexNetwork

DEFAULT_NETWORK_URL = 'https://convex.world'


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
            url = DEFAULT_NETWORK_URL
        network = ConvexNetwork(url)

        return network

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

    def is_address(self, value):
        return is_address(value)

    @abstractmethod
    def create_parser(self, sub_parser: Any) -> Any:
        pass

    @abstractmethod
    def execute(self, args: Any, output: Any) -> None:
        pass

    @property
    def name(self) -> str:
        return self._name
