"""
    Asset class to hold Ocean asset information such as asset id and metadata
"""
from eth_utils import remove_0x_prefix

from squid_py.did import (
    did_parse,
    did_to_id,
)

from ocean_py.asset.asset_base import AssetBase
from ocean_py.agent.metadata_agent import MetadataAgent
from ocean_py.agent.publish_agent import PublishAgent


# from ocean_py import logger


class Asset(AssetBase):
    def __init__(self, ocean, did=None):
        """
        init an asset class with the following:
        :param ocean: ocean object to use to connect to the ocean network
        :param did: Optional did of the asset
        """
        AssetBase.__init__(self, ocean, did)

        if self._did:
            self._id = did_to_id(did)

    def register(self, metadata, **kwargs):
        """
        Register on chain asset
        :param metadata: dict of the metadata
        :param account: account to use to register this asset
        :param service: if provided use the service from a ServiceDiscpitor
        :param price: If no service provided set the asset price
        :param timout: timeout in seconds to register the service

        :return The new asset metadata ( ddo)
        """
        
        account = kwargs.get('account')
        service = kwargs.get('service')
        price = kwargs.get('price')
        timeout = kwargs.get('timeout', 9000)

        if not account:
            raise ValueError('you must provide an account number to register the asset')


        agent = MetadataAgent(self._ocean, **kwargs)
        
        self._metadata = None
        ddo = agent.register_asset(metadata, account, service, price, timeout)
        if ddo:
            self._set_ddo(ddo)
            
        return self._metadata

    def read(self, **kwargs):
        """read the asset metadata (DDO) from the block chain, if not found return None"""
        
        agent = MetadataAgent(self._ocean, **kwargs)

        ddo = agent.read_asset(self._did)
        self._set_ddo(ddo)
        return self._metadata


    def _set_ddo(self, ddo):
        """ assign ddo values to the asset id/did and metadata proporeties"""
        self._did = ddo.did
        self._id = remove_0x_prefix(did_to_id(self._did))
        self._metadata = ddo

        
    @property
    def is_empty(self):
        """ return true if the asset is empty"""
        return self._id is None

    @staticmethod
    def is_did_valid(did):
        """ return true if the DID is in the format 'did:op:xxxxx' """
        data = did_parse(did)
        return 'data' not in data
