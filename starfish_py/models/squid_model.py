"""
    SquidModel - Access squid services using the squid-py api
"""

from starfish_py.models.model_base import ModelBase
from squid_py.service_agreement.utils import (
    get_sla_template_path,
    register_service_agreement_template
)
from squid_py import (
    ServiceAgreementTemplate,
    ServiceAgreement,
    ServiceTypes
)

# from starfish_py import logger

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
        return self._ocean._squid.register_asset(metadata, account)

    def read_asset(self, did):
        """ read the asset metadata(DDO) using the asset DID """
        return self._ocean._squid.resolve_asset_did(did)

    def search_assets(self, text, sort=None, offset=100, page=0):
        """
        Search assets from the squid API.
        """
        ddo_list = self._ocean._squid.search_assets_by_text(text, sort, offset, page)
        return ddo_list

    def is_service_agreement_template_registered(self, template_id):
        """
        :return: True if the service level agreement template has already been registered
        """
        return not self.get_service_agreement_template_owner(template_id) is None

    def get_service_agreement_template_owner(self, template_id):
        """
        :return: Owner of the registered service level agreement template, if not registered then return None
        """
        return self._ocean._squid.keeper.service_agreement.get_template_owner(template_id)

    def register_service_agreement_template(self, template_id, account):
        """
        Try to register service level agreement template using an account

        :param template_id: template id to use to register
        :param account: account to register for
        :return: The template registered
        """
        template = ServiceAgreementTemplate.from_json_file(get_sla_template_path())
        template = register_service_agreement_template(
            self._ocean._squid.keeper.service_agreement,
            account,
            template,
            self._ocean._squid.keeper.network_name
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
            service_agreement_id = self._ocean._squid.purchase_asset_service(asset.did, service_agreement.sa_definition_id, account)

        return service_agreement_id

    def consume_asset(self, asset, service_agreement_id, account):
        """
        Conusmer the asset data, by completing the payment and later returning the data for the asset

        """
        downloads_path = self._ocean._squid._downloads_path
        service_agreement = self.get_service_agreement_from_asset(asset)
        if service_agreement:
            self._ocean._squid.consume_service(service_agreement_id, asset.did, service_agreement.sa_definition_id, account)
        print(f'downloads path {downloads_path}')

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

        agreement_address = self._ocean._keeper.service_agreement.get_service_agreement_consumer(service_agreement_id)
        print(f'agreement address {agreement_address}')

        return self._ocean._squid.is_access_granted(service_agreement_id, asset.did, account_address)

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
            if not check:
                raise AssertionError
            events = _filter.get_all_entries()
            if events:
                return events[0]
            time.sleep(0.5)
