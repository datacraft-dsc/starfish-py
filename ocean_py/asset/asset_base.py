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

class AssetBase():
    def __init__(self, ocean, did=None):
        """
        init an asset class with the following:
        :param ocean: ocean object to use to connect to the ocean network
        """
        self._ocean = ocean
        self._id = None
        self._did = did

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
        return None

    @property
    def is_empty(self):
        return self._id is None

    @property
    def agent_did(self):
        """DID of the metadata agent for this asset"""
        return self._agent_did

    @property
    def did(self):
        """return the DID of the asset"""
        return self._did

    @staticmethod
    def is_did_valid(did):
        return False
