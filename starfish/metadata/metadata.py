"""
    Metadata class to handle the asset storage and addressing.

    **Currently this is in development**

"""

# from starfish import logger

class Metadata():
    """

    :param agent: agent object to used to create
    :type agent: :class:`.AgentObject`
    :param metadata: Metadata.
    :type metadata: dict

    """
    def __init__(self, agent, metadata):
        """
        init an asset class with the following:
        """
        self._agent = agent
        self._metadata = metadata

    @property
    def agent(self):
        """
        :return: Agent object
        :type: :class:`.AgentObject`
        """
        return self._agent

    @property
    def data(self):
        """
        :return: metadata of the asset
        :type: dict
        """
        return self._metadata
