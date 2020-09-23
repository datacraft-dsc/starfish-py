"""

    Test Intergation for Agents

"""
from unittest.mock import Mock

from starfish.tool.command.agent_register_command import AgentRegisterCommand
from starfish.tool.command.agent_resolve_command import AgentResolveCommand
from starfish.tool.output import Output

def test_agent_resolve_command(config):
    args = Mock()

    args.url = config['ethereum']['network']['url']
    local_agent = config['agents']['local']
    args.username = local_agent['username']
    args.password = local_agent['password']
    args.agent = local_agent['url']
    resolve = AgentResolveCommand()
    output = Output()
    resolve.execute(args, output)
    assert(output.values['did'])
    assert(output.values['ddo_text'])


def test_agent_register_command(config):
    args = Mock

    args.url = config['ethereum']['network']['url']
    local_agent = config['agents']['local']

    args.agent_url = local_agent['url']

    account = config['ethereum']['accounts']['account1']
    args.password = account['password']
    args.keyfile = account['keyfile']

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
