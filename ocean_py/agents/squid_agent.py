"""
    MetadataAgent - Agent to read/write and list metadata on the Ocean network
"""
import json
import re
import requests

from ocean_py.agents.agent import Agent
from ocean_py import logger


SQUID_AGENT_DID = 'did:op:squid-agent'

class SquidAgent(Agent):
    def __init__(self, ocean, **kwargs):
        """init a standard ocean agent, with a given DID"""
        Agent.__init__(self, ocean, **kwargs)
        self._did = SQUID_AGENT_DID

    def register(self, url, account, did=None):
        """ Squid agent does not need to register on the block chain,
        the asset is registered instead
        """
        return None
    def register_asset(self, metadata, **kwargs):
        if 'account' in kwags and 'services' in kwargs:
            result = self._ocean.squid.register(metadata, kwargs['account'], kwargs['services'])
            print(result)
