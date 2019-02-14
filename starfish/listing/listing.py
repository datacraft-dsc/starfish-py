"""
    Asset class to handle the _other_ type of asset storage and addressing.

    **Currently this is in development**

"""
from web3 import Web3
from squid_py.did import id_to_did
from eth_utils import remove_0x_prefix

from starfish.models.metadata_agent_model import MetadataAgentModel
from starfish.utils.did import did_parse
from starfish.listing import ListingObject

# from starfish import logger

class Listing(ListingObject):
    """

        :param agent: agent object that was used to create this listing
        :type agent: :class:`agent.ListingAgent`
        :param did: Optional did for this listing.
        :type did: str or None
        :param metadata: Optional metadata for the asset
        :type metadata: dict or None

    """
    def __init__(self, agent, did=None, metadata=None):
        """
        init an asset class with the following:
        """
        ListingObject.__init__(self, agent, did, metadata)

        if self._did:
            # look for did:op:xxxx/yyy, where xxx is the agent and yyy is the asset id
            data = did_parse(self._did)
            if data['id_hex'] and data['path']:
                self._agent_did = id_to_did(data['id_hex'])
                self._id = remove_0x_prefix(Web3.toHex(hexstr=data['path']))


    def read(self):
        """

        Reads the listing from the agent using the listing's DID.

        :return: metadata read for this listing, if non found then return None.
        """

        self._metadata = None
        model = MetadataAgentModel(self._ocean, did=self._agent_did)
        asset_data = model.read_asset(self._id)
        if asset_data:
            # assign the did of the agent that we registered this with
            self._id = asset_data['asset_id']
            self._metadata = asset_data['metadata_text']
        return self._metadata

    @property
    def is_empty(self):
        """
        :return: True if this asset is empty.
        """
        return self._id is None or self._agent_did is None

    @staticmethod
    def is_did_valid(did):
        """
        :return: True if the did is a valid did for this type of asset.
        """
        data = did_parse(did)
        return data['id_hex'] and data['path']
