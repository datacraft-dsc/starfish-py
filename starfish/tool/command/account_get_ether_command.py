"""

    Command Account Get Ether

"""
from typing import Any
from web3 import Web3

from starfish.account import Account

from .command_base import CommandBase


DEFAULT_AMOUNT = 10


class AccountGetEtherCommand(CommandBase):

    def __init__(self, sub_parser: Any = None) -> None:
        super().__init__('ether', sub_parser)

    def create_parser(self, sub_parser: Any) -> Any:

        parser = sub_parser.add_parser(
            self._name,
            description='Get ether for an account address',
            help='Get some ether from a faucet or transfered on a development network'

        )

        parser.add_argument(
            'address',
            help='Account address'
        )

        parser.add_argument(
            'faucet',
            metavar='network-faucet-url',
            help='Network name or faucet url'
        )

        parser.add_argument(
            'amount',
            nargs='?',
            default=DEFAULT_AMOUNT,
            help=f'Amount to request. Default {DEFAULT_AMOUNT}'
        )
        return parser

    def execute(self, args: Any, output: Any) -> None:
        if not Web3.isAddress(args.address):
            output.add_error(f'{args.address} is not an ethereum account address')
            return

        account = Account(args.address)

        faucet_url = args.faucet
        faucet_account = None
        network_setup = self.get_network_setup(args.faucet)
        if network_setup:
            if 'faucet_url' in network_setup:
                faucet_url = network_setup['faucet_url']
            if 'faucet_account' in network_setup:
                faucet_account = network_setup['faucet_account']
            network = self.get_network(args.url, network_setup['url'])
        else:
            network = self.get_network(args.url)

        if faucet_account:
            send_account = Account(faucet_account[0], faucet_account[1])
            network.send_ether(send_account, account.address, args.amount)
        else:
            network.request_ether_from_faucet(account, faucet_url)

        balance = network.get_ether_balance(account)
        output.add_line(f'Get {args.get_command} for account: {args.address} balance: {balance}')
        output.set_value('balance', balance)
        output.set_value('address', args.address)
