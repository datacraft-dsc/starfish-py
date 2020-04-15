"""

    Test tool accounts

"""
import argparse

from starfish.tool.command.account_command import AccountCommand
from starfish.tool.command.account_create_command import AccountCreateCommand
from starfish.tool.command.account_get_command import AccountGetCommand
from starfish.tool.command.account_get_ether_command import AccountGetEtherCommand
from starfish.tool.command.account_get_token_command import AccountGetTokenCommand
from starfish.tool.command.account_send_command import AccountSendCommand
from starfish.tool.command.account_send_ether_command import AccountSendEtherCommand
from starfish.tool.command.account_send_token_command import AccountSendTokenCommand

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

def test_tool_account():
    account = AccountCommand()
    parser = account.create_parser(get_sub_parser())
    assert(parser)

def test_tool_account_create():
    account = AccountCreateCommand()
    parser = account.create_parser(get_sub_parser())
    assert(parser)

def test_tool_account_get():
    account = AccountGetCommand()
    parser = account.create_parser(get_sub_parser())
    assert(parser)

def test_tool_account_get_ether():
    account = AccountGetEtherCommand()
    parser = account.create_parser(get_sub_parser())
    assert(parser)

def test_tool_account_get_token():
    account = AccountGetTokenCommand()
    parser = account.create_parser(get_sub_parser())
    assert(parser)

def test_tool_account_send():
    account = AccountSendCommand()
    parser = account.create_parser(get_sub_parser())
    assert(parser)

def test_tool_account_send_ether():
    account = AccountSendEtherCommand()
    parser = account.create_parser(get_sub_parser())
    assert(parser)

def test_tool_account_send_token():
    account = AccountSendTokenCommand()
    parser = account.create_parser(get_sub_parser())
    assert(parser)

def test_tool_network():
    account = NetworkCommand()
    parser = account.create_parser(get_sub_parser())
    assert(parser)

def test_tool_network_wait():
    account = NetworkWaitCommand()
    parser = account.create_parser(get_sub_parser())
    assert(parser)
