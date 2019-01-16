"""
    PublishAgent - Agent to access the ocean publishing and services aka Brizo
"""

from ocean_py.agent.agent_base import AgentBase
# from ocean_py import logger

class PublishAgent(AgentBase):
    def __init__(self, ocean, **kwargs):
        """init a standard ocean agent, with a given DID"""
        AgentBase.__init__(self, ocean, **kwargs)


    def publish_asset(self, asset, **kwargs):
        """
        Register an asset with the agent storage server
        :param metadata: metadata to write to the storage server

        """
        pass
