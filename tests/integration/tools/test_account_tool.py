"""

    Test tool Network Wait

"""
from unittest.mock import Mock

from starfish.tool.command.account_create_command import AccountCreateCommand
from starfish.tool.output import Output

def test_account_create_command(config):
    args = Mock()

    args.url = config.network_url
    args.password = 'test_password'
    args.keyfile = None

    network = AccountCreateCommand()
    output = Output()
    network.execute(args, output)
    print(output.values)
    assert(output.values['keyvalue'])
    assert(output.values['address'])
