#!/usr/bin/env python3

"""

    Script to provide starfish tools


"""

import argparse
import logging


from starfish.tool.create_account_command import CreateAccountCommand
from starfish.tool.get_command import GetCommand
from starfish.tool.tool_output import ToolOutput


def main():

    parser = argparse.ArgumentParser(description='Starfish Tools')

    parser.add_argument(
        '-u',
        '--url',
        help=f'URL of the network node',
    )

    parser.add_argument(
        '-d',
        '--debug',
        action='store_true',
        help=f'Debug mode on or off. Default: False',
    )

    parser.add_argument(
        '-j',
        '--json',
        action='store_true',
        help='Output data as JSON values'
    )

    command_parser = parser.add_subparsers(
        title='Starfish command',
        description='Tool command',
        help='Tool command',
        dest='command'
    )

    """
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
    """

    command_list = [
        CreateAccountCommand(command_parser),
        GetCommand(command_parser),
    ]

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    output = ToolOutput()

    for command_item in command_list:
        if command_item.is_command(args.command):
            command_item.execute(args, output)
            break

    output.printout(args.json)

    """
    command_chr = args.command[0].lower()[0]

    if command_chr == 'c':
        if args.password is None:
            print('Please provide a password for the new account')
            return
        account = Account.create(args.password)
        if args.keyfile:
            account.save_to_file(args.keyfile)
        else:
            print(account.export_key_value)
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

    elif command_chr == 't':
        if args.address is None:
            print('Please provide the account address')
            return

        account = Account(args.address, args.password)
        network.request_test_tokens(account, 10)
        print(network.get_token_balance(account))
    """


if __name__ == "__main__":
    main()
