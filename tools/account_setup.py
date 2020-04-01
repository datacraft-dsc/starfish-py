#!/usr/bin/env python3
"""

    Script to create an account and write the key file


"""

import argparse
import logging

from starfish import DNetwork
from starfish.account import Account

DEFAULT_NETWORK_URL = 'http://localhost:8545'


def main():

    parser = argparse.ArgumentParser(description='Starfish Account Setup Tool')

    parser.add_argument(
        '-u',
        '--url',
        default=DEFAULT_NETWORK_URL,
        help=f'URL of the local network node. Default: {DEFAULT_NETWORK_URL}',
    )

    parser.add_argument(
        '-d',
        '--debug',
        action='store_true',
        help=f'Debug mode on or off. Default: False',
    )

    parser.add_argument(
        '-k',
        '--keyfile',
        help='Key file to use for the account'
    )

    parser.add_argument(
        '-p',
        '--password',
        help='Password for the account'
    )

    parser.add_argument(
        '-a',
        '--address',
        help='The account address'
    )

    parser.add_argument(
        '-f',
        '--faucet',
        help='The faucet url'
    )

    parser.add_argument(
        'command',
        nargs=1,
        help='''command to execute, can be the following

            create or c - create a account
            ether or e - request ether
            '''
    )

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    network = DNetwork(args.url)
    network.load_development_contracts()

    command_chr = args.command[0].lower()[0]

    if command_chr == 'c':
        if args.password is None:
            print('Please provide a password for the new account')
            return
        account = Account.create(args.password)
        if args.keyfile:
            account.save_to_file(args.keyfile)
        else:
            print(account.key_value)
        print(account.address)
    elif command_chr == 'e':
        if args.address is None:
            print('Please provide the account address')
            return
        if args.faucet is None:
            print('Please provide the faucet url')

        account = Account(args.address, args.password)
        network.request_ether_from_faucet(account, args.faucet)
        print(network.get_ether_balance(account))


if __name__ == "__main__":
    main()
