"""
    Asset class to hold Ocean asset information such as asset id and metadata
"""
import json
import re
from web3 import Web3

from ocean_py.asset.asset_base import AssetBase
from ocean_py.agents.metadata_agent import MetadataAgent
from ocean_py.agents.squid_agent import SquidAgent
from squid_py.did import (
    did_parse,
    id_to_did,
    did_to_id,
)
# from squid_py.brizo.brizo import Brizo
from squid_py import (
    get_purchase_endpoint,
    get_service_endpoint,
    ServiceDescriptor,
    ACCESS_SERVICE_TEMPLATE_ID,
)

from ocean_py import logger


class AssetOnChain(AssetBase):
    def __init__(self, ocean, did=None):
        """
        init an asset class with the following:
        :param ocean: ocean object to use to connect to the ocean network
        :param did: Optional did of the asset
        """
        AssetBase.__init__(self, ocean, did)
        self._ddo = None

        if self._did:
            self._id = did_to_id(did)

    def register(self, metadata, account, service=None, price=None, timeout = 900):
        """
        Register an asset by writing it's meta data to the meta storage agent
        :param metadata: dict of the metadata
        :param agent: agent object for perform meta stroage
        :param **kwargs: list of args that need to be passed to the agent object
        to do the asset registration
        in the ocean agent memory storage

        :return The new asset registered, or return None on error
        """

        result = None
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
        self._ddo = None
        if ddo:
            self._id = re.sub(r'^0[xX]', '', did_to_id(ddo.did))
            self._did = ddo.did
            self._ddo = ddo


        return self._ddo

    def read(self):
        """read the asset metadata from an Ocean Agent, using the agents DID"""
        result = None
        self._ddo = self._ocean.squid.resolve_did(self._did)
        return self._ddo

    @property
    def metadata(self):
        return self._ddo

    @property
    def is_empty(self):
        return self._id is None

    @staticmethod
    def is_did_valid(did):
        data = did_parse(did)
        return data['path'] == None

