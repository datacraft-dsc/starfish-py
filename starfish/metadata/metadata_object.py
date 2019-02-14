
"""
    Basic Listing object
"""

class MetadataObject():
    def __init__(self, agent, metadata):
        """init the the Listing Object Base with the agent instance"""
        self._agent = agent
        self._metadata = metadata
        
    @property
    def agent(self):
        return self._agent

    @property
    def data(self):
        return self._metadata
