"""
    Asset class to hold Ocean asset information such as asset id and metadata
"""
from web3 import Web3

from squid_py.did import id_to_did

from eth_utils import remove_0x_prefix
from starfish_py.asset.asset_base import AssetBase
from starfish_py.models.metadata_agent_model import MetadataAgentModel
from starfish_py.utils.did import did_parse

# from starfish_py import logger

class AssetLight(AssetBase):
    def __init__(self, ocean, did=None):
        """
        init an asset class with the following:
        :param ocean: ocean object to use to connect to the ocean network
        :param did: Optional did of the asset
        """
        AssetBase.__init__(self, ocean, did)

        if self._did:
            # look for did:op:xxxx/yyy, where xxx is the agent and yyy is the asset id
            data = did_parse(self._did)
            if data['id_hex'] and data['path']:
                self._agent_did = id_to_did(data['id_hex'])
                self._id = remove_0x_prefix(Web3.toHex(hexstr=data['path']))


    def register(self, metadata, **kwargs):
        """
        Register an asset by writing it's meta data to the meta storage agent
        :param metadata: dict of the metadata
        :param agent: agent object for perform meta stroage

        :return The new asset registered, or return None on error
        """

        model = MetadataAgentModel(self._ocean)

        self._metadata = None
        asset_data = model.register_asset(metadata)
        if asset_data:
            # assign the did of the agent that we registered this with
            self._id = asset_data['asset_id']
            self._did = f'{agent.did}/{self._id}'
            self._metadata = metadata
        return self._metadata

    def read(self):
        """read the asset metadata from an Ocean Agent, using the agents DID"""

        model = MetadataAgentModel(self._ocean, did=self._agent_did)
        asset_data = model.read_asset(self._id)
        if asset_data:
            # assign the did of the agent that we registered this with
            self._id = asset_data['asset_id']
            self._metadata = asset_data['metadata_text']
        return self._metadata

    @property
    def is_empty(self):
        """return true if this asset is empty """
        return self._id is None or self._agent_did is None

    @staticmethod
    def is_did_valid(did):
        """ return true if the did is a valid did for this type of asset """
        data = did_parse(did)
        return data['id_hex'] and data['path']
