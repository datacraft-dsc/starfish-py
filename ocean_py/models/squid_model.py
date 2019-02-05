"""
    SquidModel - Access squid services using the squid-py api
"""

from ocean_py.models.model_base import ModelBase
from squid_py.service_agreement.utils import (
    get_sla_template_path,
    register_service_agreement_template
)
from squid_py import (
    ACCESS_SERVICE_TEMPLATE_ID,
    ServiceAgreementTemplate,
    ServiceAgreement,
    ServiceTypes
)

# from ocean_py import logger

class SquidModel(ModelBase):
    def __init__(self, ocean):
        """init a standard ocean agent"""
        ModelBase.__init__(self, ocean)

    def register_asset(self, metadata, account):
        """
        Register an asset with the agent storage server
        :param metadata: metadata to write to the storage server
        :param account: account to register the asset
        """
        return self._ocean.squid.register_asset(metadata, account)

    def read_asset(self, did):
        """ read the asset metadata(DDO) using the asset DID """
        return self._ocean.squid.resolve_asset_did(did)

    def search_assets(self, text, sort=None, offset=100, page=0):
        ddo_list = self._ocean.squid.search_assets_by_text(text, sort, offset, page)
        return ddo_list

    def is_service_agreement_template_registered(self, template_id):
        return self.get_service_agreement_template_owner(template_id)

    def get_service_agreement_template_owner(self, template_id):
        owner = self._ocean.squid.keeper.service_agreement.get_template_owner(template_id)
        return owner

    def register_service_agreement_template(self, template_id, account):
        template = ServiceAgreementTemplate.from_json_file(get_sla_template_path())
        template = register_service_agreement_template(
            self._ocean.squid.keeper.service_agreement,
            account,
            template,
            self._ocean.squid.keeper.network_name
        )
        return template

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

        agreement_address = self._ocean.keeper.service_agreement.get_service_agreement_consumer(service_agreement_id)

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
