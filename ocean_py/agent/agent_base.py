"""
    Agent class to provide basic functionality for all Ocean Agents
"""

class AgentBase():
    def __init__(self, ocean, **kwargs):
        """init the the AgentBase with the ocean instance"""
        self._ocean = ocean

