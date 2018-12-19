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
        if did:
            # look for did:op:xxxx/yyy, where xxx is the agent and yyy is the asset id
            data = did_parse(did)
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

        asset_data = agent.register_asset(metadata, **kwargs)
        return None

    def read_metadata(self, agent = None):
        """read the asset metadata from an Ocean Agent, using the agents DID"""

        if agent is None:
            agent = self._ocean.get_agent(self._agent_did)

        metadata_text = agent.read(self._id)
        # only return the valid metadata
        if Asset.is_metadata_valid(self._id, metadata_text):
            self._metadata_text = metadata_text
            return self.metadata
        else:
            logger.warning('asset {} metadata is not valid'.format(self._id))
        return None

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
        if not self.is_empty:
            return self._agent_did + '/' + self._id
        return None

    @staticmethod
    def is_metadata_valid(asset_id, metadata_text):
        """
        validate metadata, by calcualating the hash (asset_id) and compare this to the
        given asset_id, if both are equal then the metadata is valid
        :param asset_id: asset id to compare with
        :param metadata: dict of metadata to calculate the hash ( asset_id)
        :return bool True if metadata is valid for the asset_id provided
        """
        if metadata_text:
            # the calc asset_id from the metadata should be same as this asset_id
            metadata_id = Asset._get_asset_id_from_metadata(metadata_text)
            if metadata_id != asset_id:
                logger.debug('metdata has does not match {0} != {1}'.format(metadata_id, asset_id))
            return metadata_id == asset_id
        return False
