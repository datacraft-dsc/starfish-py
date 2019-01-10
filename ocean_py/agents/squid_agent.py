"""
    MetadataAgent - Agent to read/write and list metadata on the Ocean network
"""
import json
import re
import requests

from ocean_py.agents.agent import Agent
from ocean_py import logger
from squid_py import (
    ServiceDescriptor,
    ACCESS_SERVICE_TEMPLATE_ID,
)
from squid_py.did import (
    did_to_id,
    id_to_did,
)


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
        result = None
        if not 'account' in kwargs:
            raise ValueError('you must provide an account number to register the asset')
            
        service  = kwargs.get('service')
        if not service:
            if not 'price' in kwargs:
                raise ValueError('you must provide at least one parameter  "service=" (ServiceDiscriptor) or "price=" (Asset Price)')
            timeout = kwargs.get('timeout', 900)
            purchase_endpoint = Brizo.get_purchase_endpoint(self._ocean.squid.config)
            service_endpoint = Brizo.get_service_endpoint(self._ocean.squid.config)
            service = [ServiceDescriptor.access_service_descriptor(
                kwargs['price'],
                purchase_endpoint,
                service_endpoint, 
                timeout, 
                ACCESS_SERVICE_TEMPLATE_ID
            )]
        ddo = self._ocean.squid.register_asset(metadata, kwargs['account'], service)
        if ddo:
            result = {
                'asset_id': re.sub(r'^0[xX]', '', did_to_id(ddo.did)),
                'did': ddo.did,
                'ddo': ddo,
            }
        return result

    def read_asset(self, asset_id):
        result = None
        did = id_to_did(asset_id)
        print('loading ', did)
        ddo = self._ocean.squid.resolve_did(did)
        if ddo:
            result = {
                'asset_id': asset_id,
                'did': did,
                'ddo': ddo,
            }
        return result
            
