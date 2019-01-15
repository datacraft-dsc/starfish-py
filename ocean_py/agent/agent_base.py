"""
    Agent class to provide basic functionality for all Ocean Agents
"""

import secrets


class AgentBase():
    def __init__(self, ocean, **kwargs):
        """init the Agent with a connection client and optional DID"""
        self._ocean = ocean

