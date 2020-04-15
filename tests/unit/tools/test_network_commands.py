"""

    Test tool network

"""
import pytest


from starfish.tool.command.network_command import NetworkCommand
from starfish.tool.command.network_wait_command import NetworkWaitCommand


@pytest.fixture(scope='module')
def network_parser(sub_parser):
    network = NetworkCommand()
    network_parser = network.create_parser(sub_parser)
    assert(network_parser)
    return network_parser

def test_tool_network(network_parser):
    assert(network_parser)

def test_tool_network_wait(parser, network_parser):
    wait = NetworkWaitCommand()
    wait_parser = wait.create_parser(network_parser)
    assert(wait_parser)
    args = parser.parse_args(['network', 'wait'])
    assert(args)
