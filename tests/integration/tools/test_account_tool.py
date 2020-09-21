"""

    Test tool Network Wait

"""
from unittest.mock import Mock

from starfish.tool.command.account_create_command import AccountCreateCommand
from starfish.tool.command.account_balance_command import AccountBalanceCommand
from starfish.tool.output import Output

def test_account_create_command(config):
    args = Mock()

    args.url = config['ethereum']['network']['url']
    args.password = 'test_password'
    args.keyfile = None

    network = AccountCreateCommand()
    output = Output()
    network.execute(args, output)
    print(output.values)
    assert(output.values['keyvalue'])
    assert(output.values['address'])

def test_account_balance(config):

    args = Mock()
    args.address = config['ethereum']['accounts']['account1']['address']
    args.url = config['ethereum']['network']['url']
    network = AccountBalanceCommand()
    output = Output()
    network.execute(args, output)
    assert(output.values['token'])
    assert(output.values['ether'])

