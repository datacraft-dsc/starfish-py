"""
    Agent class to provide basic functionality for all Ocean Agents
"""

import secrets

from squid_py.ddo import DDO
from squid_py.did_resolver import DIDResolver
from squid_py.did import id_to_did

class Agent():
    def __init__(self, ocean, **kwargs):
        """init the Agent with a connection client and optional DID"""
        self._ocean = ocean
        self._did = kwargs.get('did', None)
        self._ddo = None
        # if DID then try to load in the linked DDO
        if self._did:
            self._ddo = self._resolve_did_to_ddo(self._did)

    def register_ddo(self, did, ddo, account):
        """register a ddo object on the block chain for this agent"""
        # register/update the did->ddo to the block chain
        return self._ocean.keeper.didregistry.register(did, ddo=ddo, account=account)

    @property
    def ddo(self):
        """return the DDO stored for this agent"""
        return self._ddo

    @property
    def did(self):
        """return the DID used for this agent"""
        return self._did

    @property
    def is_empty(self):
        """return True if this agent object is empty"""
        return self._did is None

    @property
    def is_valid(self):
        """return True if this agent has a valid ddo"""
        return self._ddo and self._ddo.is_valid


    def _resolve_did_to_ddo(self, did):
        """resolve a DID to a given DDO, return the DDO if found"""
        did_resolver = DIDResolver(self._ocean.web3, self._ocean.keeper.didregistry)
        resolved = did_resolver.resolve(did)
        if resolved and resolved.is_ddo:
            ddo = DDO(json_text=resolved.value)
            return ddo
        return None

    def _get_endpoint(self, name):
        """return the endpoint based on the service name"""
        if self._ddo:
            service = self._ddo.get_service(name)
            if service:
                return service.get_endpoint()
        return None
