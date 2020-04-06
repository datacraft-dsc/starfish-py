"""

    Command Send Token

"""
import logging

from web3 import Web3

from starfish.account import Account

from .command_base import CommandBase

logger = logging.getLogger(__name__)


class SendTokenCommand(CommandBase):

    def __init__(self, subparser):
        super().__init__('token', subparser)

    def create_parser(self, subparser):

        parser = subparser.add_parser(
            self._name,
            description='Send tokens for an account address',
            help='Send tokens from one account to the another'
        )

        parser.add_argument(
            'address',
            help='Account address'
        )

        parser.add_argument(
            'password',
            help='Account password'
        )

        parser.add_argument(
            'keyfile',
            help='Account keyfile'
        )

        parser.add_argument(
            'to_address',
            help='Address to send data too',
        )

        parser.add_argument(
            'amount',
            help=f'Amount to send'
        )

    def execute(self, args, output):
        if not Web3.isAddress(args.address):
            output.add_error(f'{args.address} is not an ethereum account address')
            return

        account = Account(args.address, args.password, key_file=args.keyfile)
        amount = float(args.amount)
        to_address = args.to_address

        network = self.get_network(args.url)
        logger.debug(f'sending tokens from account {account.address} to account {to_address}')
        network.send_token(account, to_address, amount)

        balance = network.get_token_balance(account)
        output.add_line(f'Send {amount} tokens from account: {args.address} to account {to_address}')
        output.set_value('balance', balance)
        output.set_value('from_address', args.address)
        output.set_value('to_address', args.to_address)
        output.set_value('amount', amount)
