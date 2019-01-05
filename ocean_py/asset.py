"""
    Asset class to hold Ocean asset information such as asset id and metadata
"""
import json
import re
from web3 import Web3

from ocean_py.agents.metadata_agent import MetadataAgent
from ocean_py.agents.squid_agent import SquidAgent
from squid_py.did import (
    did_parse,
    id_to_did,
)
from ocean_py import logger

class Asset():
    def __init__(self, ocean, did=None):
        """
        init an asset class with the following:
        :param ocean: ocean object to use to connect to the ocean network
        :param did: Optional did of the asset
        """
        self._ocean = ocean
        self._id = None
        self._metadata_text = None
        self._agent_did = None
        self._asset_data = None
        if did:
            # look for did:op:xxxx/yyy, where xxx is the agent and yyy is the asset id
            data = did_parse(did)
            print(data)
            if data['id_hex'] and data['path']:
                self._agent_did = id_to_did(data['id_hex'])
                self._id = re.sub(r'^0[xX]', '', Web3.toHex(hexstr=data['path']))
        
    def register(self, metadata, agent, **kwargs):
        """
        Register an asset by writing it's meta data to the meta storage agent
        :param metadata: dict of the metadata
        :param agent: agent object for perform meta stroage
        :param **kwargs: list of args that need to be passed to the agent object
        to do the asset registration
        in the ocean agent memory storage

        :return The new asset registered, or return None on error
        """
        
        self._asset_data = agent.register_asset(metadata, **kwargs)
        if self._asset_data:
            # assign the did of the agent that we registered this with
            self._agent_did = agent.did
            self._id = self._asset_data['asset_id']

        return self._asset_data

    def read(self, agent = None):
        """read the asset metadata from an Ocean Agent, using the agents DID"""

        if agent is None:
            agent = self._ocean.get_agent(self._agent_did)

        self._asset_data = agent.read_asset(self._id)
        if self._asset_data:
            # assign the did of the agent that we registered this with
            self._agent_did = agent.did
            # self._id = self._asset_data['asset_id']        
        return self._asset_data

    @property
    def asset_id(self):
        """return the asset id"""
        return self._id

    @property
    def metadata(self):
        """return the associated metadata for this assset"""
        if self._metadata_text:
            return json.loads(self._metadata_text)
        return None

    @property
    def is_empty(self):
        return self._id is None or self._agent_did is None

    @property
    def agent_did(self):
        """DID of the metadata agent for this asset"""
        return self._agent_did

    @property
    def did(self):
        """return the DID of the asset"""
        if self._agent_did:
            return self._agent_did + '/' + self._id
        return None

