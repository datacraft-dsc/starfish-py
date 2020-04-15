"""

    Test tool Network Wait

"""
from unittest.mock import Mock

from starfish.tool.command.network_wait_command import NetworkWaitCommand
from starfish.tool.output import Output

def test_network_wait_command(config):
    args = Mock()

    args.url = config.network_url
    args.timeout = 20

    network = NetworkWaitCommand()
    output = Output()
    network.execute(args, output)
    assert(output.values['is_ready'] == True)