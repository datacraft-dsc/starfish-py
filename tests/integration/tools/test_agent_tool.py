"""

    Test Intergation for Agents

"""
from unittest.mock import Mock

from starfish.tool.command.agent_register_command import AgentRegisterCommand
from starfish.tool.command.agent_resolve_command import AgentResolveCommand
from starfish.tool.output import Output

def test_agent_resolve_command(config):
    args = Mock()

    args.url = config.network_url
    remote_agent = config.agent_list['remote']
    args.username = remote_agent['username']
    args.password = remote_agent['password']
    args.agent = remote_agent['url']
    resolve = AgentResolveCommand()
    output = Output()
    resolve.execute(args, output)
    assert(output.values['did'])
    assert(output.values['ddo_text'])


def test_agent_register_command(config):
    args = Mock

    args.url = config.network_url
    remote_agent = config.agent_list['remote']

    args.agent_url = remote_agent['url']

    args.address = config.account_1['address']
    args.password = config.account_1['password']
    args.keyfile = config.account_1['keyfile']

    # all services
    args.service_list = None

    register = AgentRegisterCommand()
    output = Output()
    register.execute(args, output)
    assert(output.values['did'])
    assert(output.values['ddo_text'])


    # register only a list of services
    args.service_list = 'meta, storage'

    register = AgentRegisterCommand()
    output = Output()
    register.execute(args, output)
    assert(output.values['did'])
    assert(output.values['ddo_text'])
