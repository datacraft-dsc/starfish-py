"""
    MetadataAgent - Agent to access the off chain meta storage in squid aka Aquarius
"""

from squid_py.brizo.brizo import Brizo

from squid_py import (
    ServiceDescriptor,
    ACCESS_SERVICE_TEMPLATE_ID,
)

from ocean_py.agent.agent_base import AgentBase
# from ocean_py import logger

class MetadataAgent(AgentBase):
    def __init__(self, ocean, **kwargs):
        """init a standard ocean agent, with a given DID"""
        AgentBase.__init__(self, ocean, **kwargs)

    def register_asset(self, metadata, account, service=None, price=None, timeout=9000):
        """
        Register an asset with the agent storage server
        :param metadata: metadata to write to the storage server
        :param account: account to register the asset
        :param service: optional service object to use for registration or..
        :param price: optional price of the asset to register, you need to provide price or service
        :param timout: optional timeout to wait for registration confirmation
        """
        if not account:
            raise ValueError('you must provide an account number to register the asset')

        if not service:
            if not price:
                raise ValueError('you must provide at least one parameter  "service=" (ServiceDiscriptor) or "price=" (Asset Price)')
            timeout = timeout
            purchase_endpoint = Brizo.get_purchase_endpoint(self._ocean.squid.config)
            service_endpoint = Brizo.get_service_endpoint(self._ocean.squid.config)
            service = [ServiceDescriptor.access_service_descriptor(
                price,
                purchase_endpoint,
                service_endpoint,
                timeout,
                ACCESS_SERVICE_TEMPLATE_ID
            )]
        # TODO: we may need to see if we can pass our own service descriptors
        # instead of relying squid to create them for us.
        return self._ocean.squid.register_asset(metadata, account)

    def read_asset(self, did):
        """ read the asset metadata(DDO) using the asset DID """
        return self._ocean.squid.resolve_did(did)
