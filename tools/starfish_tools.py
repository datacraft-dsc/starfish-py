#!/usr/bin/env python3

"""

    Script to provide starfish tools


"""

import argparse
import logging


from starfish.tool.create_account_command import CreateAccountCommand
from starfish.tool.get_command import GetCommand
from starfish.tool.send_command import SendCommand
from starfish.tool.tool_output import ToolOutput
from starfish.tool.wait_network_command import WaitNetworkCommand


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

    command_list = [
        CreateAccountCommand(command_parser),
        GetCommand(command_parser),
        SendCommand(command_parser),
        WaitNetworkCommand(command_parser)
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


if __name__ == "__main__":
    main()
