
"""
    Basic Listing object
"""

class ListingObject():
    def __init__(self, agent, did, metadata):
        """init the the Listing Object Base with the agent instance"""
        self._agent = agent
        self._did = did
        self._metadata = metadata

    @property
    def agent(self):
        """

        :return: Agent object that created this listing
        :type: :class:`.SquidAgent`
        """
        return self._agent

    @property
    def did(self):
        """

        :return: DID of the listing
        :type: str
        """
        return self._did

    @property
    def metadata(self):
        """

        :return: metadata held by the listing
        :type: dict
        """
        return self._metadata
