"""
    Asset class to hold Ocean asset information such as asset id and metadata
"""
from eth_utils import remove_0x_prefix

from squid_py.did import (
    did_parse,
    did_to_id,
)

# next version of squid...
# from squid_py.brizo.brizo import Brizo

from squid_py import (
    get_purchase_endpoint,
    get_service_endpoint,
    ServiceDescriptor,
    ACCESS_SERVICE_TEMPLATE_ID,
)
from ocean_py.asset.asset_base import AssetBase

# from ocean_py import logger


class AssetOnChain(AssetBase):
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
        timeout = kwargs.get('timeout', 900)

        if not account:
            raise ValueError('you must provide an account number to register the asset')

        if not service:
            if not price:
                raise ValueError('you must provide at least one parameter  "service=" (ServiceDiscriptor) or "price=" (Asset Price)')
            timeout = timeout
            purchase_endpoint = get_purchase_endpoint(self._ocean.squid.config)
            service_endpoint = get_service_endpoint(self._ocean.squid.config)
            service = [ServiceDescriptor.access_service_descriptor(
                price,
                purchase_endpoint,
                service_endpoint,
                timeout,
                ACCESS_SERVICE_TEMPLATE_ID
            )]
        ddo = self._ocean.squid.register_asset(metadata, account, service)
        self._metadata = None
        if ddo:
            self._id = remove_0x_prefix(did_to_id(ddo.did))
            self._did = ddo.did
            self._metadata = ddo


        return self._metadata

    def read(self):
        """read the asset metadata (DDO) from the block chain, if not found return None"""
        self._metadata = self._ocean.squid.resolve_did(self._did)
        return self._metadata


    @property
    def is_empty(self):
        """ return true if the asset is empty"""
        return self._id is None

    @staticmethod
    def is_did_valid(did):
        """ return true if the DID is in the format 'did:op:xxxxx' """
        data = did_parse(did)
        return data['path'] is None
