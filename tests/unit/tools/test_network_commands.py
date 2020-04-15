"""

    Test tool network

"""
import argparse


from starfish.tool.command.network_command import NetworkCommand
from starfish.tool.command.network_wait_command import NetworkWaitCommand


def get_sub_parser():
    parser = argparse.ArgumentParser(description='Starfish Tools')

    sub_parser = parser.add_subparsers(
        title='Starfish command',
        description='Tool command',
        help='Tool command',
        dest='command'
    )
    return sub_parser

def test_tool_network():
    account = NetworkCommand()
    parser = account.create_parser(get_sub_parser())
    assert(parser)

def test_tool_network_wait():
    account = NetworkWaitCommand()
    parser = account.create_parser(get_sub_parser())
    assert(parser)
