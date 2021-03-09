"""

    Test Intergation for Agents

"""
from unittest.mock import Mock

from starfish.tool.command.agent_register_command import AgentRegisterCommand
from starfish.tool.command.agent_resolve_command import AgentResolveCommand
from starfish.tool.command.account_create_command import AccountCreateCommand
from starfish.tool.command.account_get_token_command import AccountGetTokenCommand
from starfish.tool.output import Output

TEST_AMOUNT = 100000000

def test_agent_resolve_command(config):
    args = Mock()

    args.url = config['convex']['network']['url']
    local_agent = config['agents']['surfer']
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

    args.url = config['convex']['network']['url']
    local_agent = config['agents']['surfer']

    args.agent_url = local_agent['url']

    account = config['convex']['accounts']['account1']
    args.password = account['password']
    args.keyfile = account['keyfile']

    # create a new address
    command = AccountCreateCommand()
    output = Output()
    command.execute(args, output)
    assert(output.values['address'])
    args.address = output.values['address']

    args.amount = TEST_AMOUNT
    command = AccountGetTokenCommand()
    output = Output()
    command.execute(args, output)

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
