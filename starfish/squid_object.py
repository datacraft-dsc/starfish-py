
"""
    Basic squid object
"""

class SquidObject():
    def __init__(self, agent):
        """init the the Squid Object Base with the agent instance"""
        self._agent = agent


    @property
    def squid_model(self):
        return self._agent.squid_model
        
    @property
    def agent(self):
        return self._agent
