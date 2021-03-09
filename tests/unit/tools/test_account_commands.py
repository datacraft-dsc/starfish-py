"""

    Test tool accounts

"""
import argparse
import pytest

from starfish.tool.command.account_command import AccountCommand
from starfish.tool.command.account_balance_command import AccountBalanceCommand
from starfish.tool.command.account_create_command import AccountCreateCommand
from starfish.tool.command.account_get_command import AccountGetCommand
from starfish.tool.command.account_get_token_command import AccountGetTokenCommand
from starfish.tool.command.account_send_command import AccountSendCommand
from starfish.tool.command.account_send_token_command import AccountSendTokenCommand



@pytest.fixture(scope='module')
def account_parser(sub_parser):
    account = AccountCommand()
    account_parser = account.create_parser(sub_parser)
    assert(account_parser)
    return account_parser

@pytest.fixture(scope='module')
def account_get_parser(account_parser):
    account_get = AccountGetCommand()
    get_parser = account_get.create_parser(account_parser)
    assert(get_parser)
    return get_parser

@pytest.fixture(scope='module')
def account_send_parser(account_parser):
    account_send = AccountSendCommand()
    send_parser = account_send.create_parser(account_parser)
    assert(send_parser)
    return send_parser


def test_tool_account(account_parser):
    assert(account_parser)

def test_tool_account_create(parser, account_parser):
    create = AccountCreateCommand()
    create_parser = create.create_parser(account_parser)
    assert(create_parser)
    args = parser.parse_args(['account', 'create', 'password'])
    assert(args)

def test_tool_account_balance(parser, account_parser):
    balance = AccountBalanceCommand()
    balance_parser = balance.create_parser(account_parser)
    assert(balance_parser)
    args = parser.parse_args(['account', 'balance', 'address'])
    assert(args)

def test_tool_account_get(parser, account_get_parser):
    assert(account_get_parser)
    args = parser.parse_args(['account', 'get'])
    assert(args)

def test_tool_account_get_token(parser, account_get_parser):
    account = AccountGetTokenCommand()
    token_parser = account.create_parser(account_get_parser)
    assert(token_parser)
    args = parser.parse_args(['account', 'get', 'token', 'address', 'password', 'keyfile'])
    assert(args)

def test_tool_account_send(parser, account_send_parser):
    assert(account_send_parser)
    args = parser.parse_args(['account', 'send'])
    assert(args)


def test_tool_account_send_token(parser, account_send_parser):
    account = AccountSendTokenCommand()
    token_parser = account.create_parser(account_send_parser)
    assert(token_parser)
    args = parser.parse_args(['account', 'send', 'token', 'address', 'password', 'keyfile', 'to_address', 'amount'])
    assert(args)


