
"""
    Basic Purchase object
"""

class PurchaseObject():
    def __init__(self, agent, listing):
        """init the the Purchase Object Base with the agent instance"""
        self._agent = agent
        self._listing = listing

    @property
    def agent(self):
        """
        :return: Agent object
        :type: :class:`.AgentObject`
        """
        return self._agent

    @property
    def listing(self):
        """
        :return: Listing object
        :type: :class:`.ListingObject'`
        """
        return self._listing
