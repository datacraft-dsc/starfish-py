"""

    Test tool Network Wait

"""
from unittest.mock import Mock

from starfish.tool.command.account_create_command import AccountCreateCommand
from starfish.tool.command.account_balance_command import AccountBalanceCommand
from starfish.tool.command.account_get_token_command import AccountGetTokenCommand
from starfish.tool.output import Output


TEST_AMOUNT = 1000000

def test_account_create_command(config):
    args = Mock()

    args.url = config['convex']['network']['url']
    args.password = 'test_password'
    args.keyfile = None

    command = AccountCreateCommand()
    output = Output()
    command.execute(args, output)
    print(output.values)
    assert(output.values['public_key'])
    assert(output.values['address'])

def test_account_balance(config):

    args = Mock()
    args.url = config['convex']['network']['url']
    args.password = 'test_password'
    args.keyfile = None

    command = AccountCreateCommand()
    output = Output()
    command.execute(args, output)
    assert(output.values['address'])
    args.address = output.values['address']
    assert(output.values['export_key'])
    args.keytext = output.values['export_key']

    args.amount = TEST_AMOUNT
    command = AccountGetTokenCommand()
    output = Output()
    command.execute(args, output)

    command = AccountBalanceCommand()
    output = Output()
    command.execute(args, output)
    assert(output.values['token'] == TEST_AMOUNT)

