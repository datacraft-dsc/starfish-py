
"""
    Basic Listing object
"""

class ListingObject():
    def __init__(self, agent, did):
        """init the the Listing Object Base with the agent instance"""
        self._agent = agent
        self._did = did
        
    @property
    def agent(self):
        return self._agent

    @property
    def did(self):
        return self._did
