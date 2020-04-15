"""

    Test Intergation for Agents

"""
from unittest.mock import Mock

from starfish.tool.command.agent_resolve_command import AgentResolveCommand
from starfish.tool.output import Output

def test_agent_resolve_command(config):
    args = Mock()

    args.url = config.network_url
    remote_agent = config.agent_list['remote']
    args.username = remote_agent['username']
    args.password = remote_agent['password']
    args.agent = remote_agent['url']
    network = AgentResolveCommand()
    output = Output()
    network.execute(args, output)
    assert(output.values['type'] == 'url')
    assert(output.values['agent'])
    assert(output.values['ddo_text'])
