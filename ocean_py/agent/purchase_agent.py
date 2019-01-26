"""
    PublishAgent - Agent to access the ocean publishing and services aka Brizo
"""
import time
from web3 import Web3
from squid_py import ServiceAgreement, ServiceTypes

from ocean_py.agent.agent_base import AgentBase
# from ocean_py import logger

class PurchaseAgent(AgentBase):
    def __init__(self, ocean):
        """init a standard ocean agent"""
        AgentBase.__init__(self, ocean)


    def purchase_asset(self, asset, account):
        """
        Purchase an asset with the agent storage server
        :param asset: asset to purchase
        :param account: account unlocked and has sufficient funds to buy this asset
        
        :return: service_agreement_id of the purchase or None if no purchase could be made
        """
        service_agreement_id = None
        service_agreement = self.get_service_agreement_from_asset(asset)
        if service_agreement:
            service_agreement_id = self._ocean.squid.purchase_asset_service(asset.did, service_agreement.sa_definition_id, account)

        return service_agreement_id

    def consume_asset(self, asset, service_agreement_id, account):
        """
        Conusmer the asset data, by completing the payment and later returning the data for the asset
        
        """
        downloads_path = self._ocean.squid._downloads_path
        service_agreement = self.get_service_agreement_from_asset(asset)
        if service_agreement:
            self._ocean.squid.consume_service(service_agreement_id, asset.did, service_agreement.sa_definition_id, account)

    def is_access_granted_for_asset(self, asset, service_agreement_id, account):
        """
        Return true if we have access to the asset's data using the service_agreement_id and account used 
        to purchase this asset
        """
        account_address = None
        if isinstance(account, object):
            account_address = account.address
        elif isinstance(account, str):
            account_address = account
        else:
            raise TypeError(f'You need to pass an account object or account address')

        print(service_agreement_id, account_address)
        agreement_address = self._ocean.keeper.service_agreement.get_service_agreement_consumer(service_agreement_id)
        print('agreement_address=', agreement_address, service_agreement_id)

        return self._ocean.squid.is_access_granted(service_agreement_id, asset.did, account_address)

    def get_service_agreement_from_asset(self, asset):
        """
        return the service agreement definition for this asset
        """
        service_agreement = None
        ddo = asset.ddo

        if ddo:
            service = ddo.get_service(service_type=ServiceTypes.ASSET_ACCESS)
            assert ServiceAgreement.SERVICE_DEFINITION_ID in service.as_dictionary()
            service_agreement = ServiceAgreement.from_service_dict(service.as_dictionary())
        return service_agreement

    @staticmethod
    def wait_for_event(event, arg_filter, wait_iterations=20):
        """
        Method used to wait for the service agreements to complete
        """
        _filter = event.createFilter(fromBlock=0, argument_filters=arg_filter)
        for check in range(wait_iterations):
            events = _filter.get_all_entries()
            if events:
                return events[0]
            time.sleep(0.5)
