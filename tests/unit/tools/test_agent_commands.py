"""

    Test tool agent

"""
import pytest


from starfish.tool.command.agent_command import AgentCommand
from starfish.tool.command.agent_resolve_command import AgentResolveCommand


@pytest.fixture(scope='module')
def agent_parser(sub_parser):
    agent = AgentCommand()
    agent_parser = agent.create_parser(sub_parser)
    assert(agent_parser)
    return agent_parser

def test_tool_agent(agent_parser):
    assert(agent_parser)

def test_tool_agent_resolve(parser, agent_parser):
    agent_resolve = AgentResolveCommand()
    resolve_parser = agent_resolve.create_parser(agent_parser)
    assert(resolve_parser)

    args = parser.parse_args(['agent', 'resolve', 'agent_did'])
    assert(args)

