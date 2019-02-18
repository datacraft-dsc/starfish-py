"""
    SquidModel - Access squid services using the squid-py api
"""

from squid_py.agreements.utils import (
    get_sla_template_path,
    register_service_agreement_template
)

from squid_py.agreements.service_agreement_template import ServiceAgreementTemplate
from squid_py.agreements.service_types import ACCESS_SERVICE_TEMPLATE_ID
from squid_py.agreements.service_agreement import ServiceAgreement
from squid_py.agreements.service_types import ServiceTypes


# from starfish import logger

class SquidModel():
    def __init__(self, ocean, options=None):
        """init a standard ocean object"""
        self._ocean = ocean

        if not isinstance(options, dict):
            options = {}

        self._aquarius_url = options.get('aquarius_url', 'http://localhost:5000')
        self._brizo_url = options.get('brizo_url', 'http://localhost:8030')
        self._secret_store_url = options.get('secret_store_url', 'http://localhost:12001')
        self._storage_path = options.get('storage_path', 'squid_py.db')
        self._parity_url = options.get('parity_url', self._ocean.keeper_url)

        self._squid_ocean = self.get_squid_ocean()

    def register_asset(self, metadata, account):
        """
        Register an asset with the agent storage server
        :param metadata: metadata to write to the storage server
        :param account: account to register the asset
        """
        squid_ocean = self.get_squid_ocean(account)
        return squid_ocean.register_asset(metadata, account._squid_account)

    def read_asset(self, did):
        """ read the asset metadata(DDO) using the asset DID """
        return self._squid_ocean.resolve_asset_did(did)

    def search_assets(self, text, sort=None, offset=100, page=0):
        """
        Search assets from the squid API.
        """
        ddo_list = self._squid_ocean.search_assets_by_text(text, sort, offset, page)
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
        return self._squid_ocean.keeper.service_agreement.get_template_owner(template_id)

    def register_service_agreement_template(self, template_id, account):
        """
        Try to register service level agreement template using an account

        :param template_id: template id to use to register
        :param account: account to register for
        :return: The template registered
        """
        template = ServiceAgreementTemplate.from_json_file(get_sla_template_path())
        template = register_service_agreement_template(
            self._squid_ocean.keeper.service_agreement,
            account._squid_account,
            template,
            self._squid_ocean.keeper.network_name
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
            service_agreement_id = self._squid_ocean.purchase_asset_service(asset.did, service_agreement.sa_definition_id, account._squid_account)

        return service_agreement_id

    def consume_asset(self, asset, service_agreement_id, account, download_path):
        """
        Conusmer the asset data, by completing the payment and later returning the data for the asset

        """
        squid_ocean = self.get_squid_ocean(account, download_path)
        service_agreement = self.get_service_agreement_from_asset(asset)
        if service_agreement:
            squid_ocean.consume_service(service_agreement_id, asset.did, service_agreement.sa_definition_id, account._squid_account)
        print(f'downloads path {download_path}')

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

#        agreement_address = self._squid_ocean.keeper.service_agreement.get_service_agreement_consumer(service_agreement_id)

        return self._squid_ocean.is_access_granted(service_agreement_id, asset.did, account_address)

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

    def register_ddo(self, did, ddo, account):
        """
        register a ddo object on the block chain for this agent
        """
        # register/update the did->ddo to the block chain
        return self._ocean._keeper.did_registry.register(did, ddo=ddo, account=account)


    def _as_config_dict(self, options=None):
        """

        Return a set of config values, so that squid can read.

        :param options: optional values to add to the dict to send to squid
        :type options: dict or None


        :return: a dict that is compatiable with the current supported version of squid-py.
        :type: dict

        """
        data = {
            'keeper-contracts': {
                'keeper.url': self._ocean.keeper_url,
                'keeper.path': self._ocean.contracts_path,
                'secret_store.url': self._secret_store_url,
                'parity.url': self._parity_url,
            },
            'resources': {
                'aquarius.url': self._aquarius_url,
                'brizo.url': self._brizo_url,
                'storage.path': self._storage_path,
            }
        }
        if options:
            if 'parity_address' in options:
                data['keeper-contracts']['parity.address'] = options['parity_address']
            if 'parity_password' in options:
                data['keeper-contracts']['parity.password'] = options['parity_password']
            if 'download_path' in options:
                data['resources']['downloads.path'] = options['download_path']

        return data

    @property
    def accounts(self):
        return self._squid_ocean.get_accounts()

    @property
    def aquarius_url(self):
        return self._aquarius_url

    @property
    def brizo_url(self):
        return self._brizo_url

    def get_squid_ocean(self, account = None, download_path=None):
        """

        Return an instance of squid for an account

        """

        options = {}
        if account:
            options['parity_address'] = account.address
            options['parity_password'] = account.password

        if download_path:
            options['download_path'] = download_path


        config_params = self._as_config_dict(options)
        config = SquidConfig(options_dict=config_params)
        return SquidOcean(config)
