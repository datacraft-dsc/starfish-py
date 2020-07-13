"""

    Command Account Get ..

"""
from typing import Any
from web3 import Web3


from .command_base import CommandBase

DEFAULT_AMOUNT = 10


class AccountBalanceCommand(CommandBase):

    def __init__(self, sub_parser: Any = None) -> None:
        self._command_list = []
        super().__init__('balance', sub_parser)

    def create_parser(self, sub_parser: Any) -> Any:

        parser = sub_parser.add_parser(
            self._name,
            description='Get balance of ether and tokens for an account address',
            help='Get balance of an account'

        )

        parser.add_argument(
            'address',
            help='Account address to get the balance'
        )
        return parser

    def execute(self, args: Any, output: Any) -> None:
        if not Web3.isAddress(args.address):
            output.add_error(f'{args.address} is not an ethereum account address')
            return

        network = self.get_network(args.url)
        ether_balance = network.get_ether_balance(args.address)
        token_balance = network.get_token_balance(args.address)
        output.add_line(f'ether balance: {ether_balance}')
        output.add_line(f'token balance: {token_balance}')
        output.set_value('ether', ether_balance)
        output.set_value('token', token_balance)
