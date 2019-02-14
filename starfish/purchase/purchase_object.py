
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
        return self._agent

    @property
    def listing(self):
        return self._listing
