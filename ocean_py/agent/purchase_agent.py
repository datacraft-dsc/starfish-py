"""
    PublishAgent - Agent to access the ocean publishing and services aka Brizo
"""

from squid_py import ServiceAgreement, ServiceTypes

from ocean_py.agent.agent_base import AgentBase
# from ocean_py import logger

class PurchaseAgent(AgentBase):
    def __init__(self, ocean, **kwargs):
        """init a standard ocean agent, with a given DID"""
        AgentBase.__init__(self, ocean, **kwargs)


    def purchase_asset(self, asset, account):
        """
        Register an asset with the agent storage server
        :param asset: asset to purchase
        :param account: account to use for buying this asset
        """
        
        ddo = asset.metadata
        service = ddo.get_service(service_type=ServiceTypes.ASSET_ACCESS)
        assert ServiceAgreement.SERVICE_DEFINITION_ID in service.as_dictionary()
        sa = ServiceAgreement.from_service_dict(service.as_dictionary())
        self._ocean.squid.purchase_asset_service(asset.did, sa.sa_definition_id, account)

