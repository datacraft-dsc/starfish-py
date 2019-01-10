"""
    Asset class to hold Ocean asset information such as asset id and metadata
"""
import re
from web3 import Web3

from squid_py.did import (
    did_parse,
    id_to_did,
)

from ocean_py.asset.asset_base import AssetBase
# from ocean_py import logger

class AssetOffChain(AssetBase):
    def __init__(self, ocean, did=None, agent=None, **kwargs):
        """
        init an asset class with the following:
        :param ocean: ocean object to use to connect to the ocean network
        :param did: Optional did of the asset
        """
        AssetBase.__init__(self, ocean, did)

        if agent:
            self._agent = agent

        if self._did:
            # look for did:op:xxxx/yyy, where xxx is the agent and yyy is the asset id
            data = did_parse(self._did)
            if data['id_hex'] and data['path']:
                agent_did = id_to_did(data['id_hex'])
                if not self._agent:
                    self._agent = ocean.resolve_agent(agent_did, **kwargs)
                self._id = re.sub(r'^0[xX]', '', Web3.toHex(hexstr=data['path']))

    def register(self, metadata, **kwargs):
        """
        Register an asset by writing it's meta data to the meta storage agent
        :param metadata: dict of the metadata
        :param agent: agent object for perform meta stroage
        :param **kwargs: list of args that need to be passed to the agent object
        to do the asset registration
        in the ocean agent memory storage

        :return The new asset registered, or return None on error
        """

        self._metadata = None
        asset_data = self._agent.register_asset(metadata, **kwargs)
        if asset_data:
            # assign the did of the agent that we registered this with
            self._id = asset_data['asset_id']
            self._did = '{0}/{1}'.format(self._agent.did, self._id)
            self._metadata = metadata

        return self._metadata

    def read(self):
        """read the asset metadata from an Ocean Agent, using the agents DID"""

        asset_data = self._agent.read_asset(self._id)
        if asset_data:
            # assign the did of the agent that we registered this with
            self._id = asset_data['asset_id']
            self._metadata = asset_data['metadata_text']
        return self._metadata


    @property
    def is_empty(self):
        return self._id is None or self._agent is None

    @property
    def agent(self):
        """DID of the metadata agent for this asset"""
        return self._agent

    @staticmethod
    def is_did_valid(did):
        data = did_parse(did)
        return data['id_hex'] and data['path']
