"""
    PublishAgent - Agent to access the ocean publishing and services aka Brizo
"""
import time
from web3 import Web3
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
        
        ddo = asset.ddo
        if ddo:
            service = ddo.get_service(service_type=ServiceTypes.ASSET_ACCESS)
            assert ServiceAgreement.SERVICE_DEFINITION_ID in service.as_dictionary()
            sa = ServiceAgreement.from_service_dict(service.as_dictionary())
            service_agreement_id = self._ocean.squid.purchase_asset_service(asset.did, sa.sa_definition_id, account)
            
            assert service_agreement_id, 'agreement id is None.'
            print('got new service agreement id:', service_agreement_id)
            filter1 = {'serviceAgreementId': Web3.toBytes(hexstr=service_agreement_id)}
            filter_2 = {'serviceId': Web3.toBytes(hexstr=service_agreement_id)}
            executed = PurchaseAgent.wait_for_event(
                self._ocean.keeper.service_agreement.events.ExecuteAgreement, 
                filter1
            )
            assert executed
            locked = PurchaseAgent.wait_for_event(
                self._ocean.squid.keeper.payment_conditions.events.PaymentLocked,
                filter_2
            )
            assert locked
            granted = PurchaseAgent.wait_for_event(
                self._ocean.squid.keeper.access_conditions.events.AccessGranted,
                filter_2
            )
            assert granted
            released = PurchaseAgent.wait_for_event(
                self._ocean.squid.keeper.payment_conditions.events.PaymentReleased, 
                filter_2
            )
            assert released
            fulfilled = PurchaseAgent.wait_for_event(
                self._ocean.squid.keeper.service_agreement.events.AgreementFulfilled, 
                filter1
            )
            assert fulfilled
            print('agreement was fulfilled.')
            return True
            
        return False

    @staticmethod
    def wait_for_event(event, arg_filter, wait_iterations=20):
        _filter = event.createFilter(fromBlock=0, argument_filters=arg_filter)
        for check in range(wait_iterations):
            events = _filter.get_all_entries()
            if events:
                return events[0]
            time.sleep(0.5)
