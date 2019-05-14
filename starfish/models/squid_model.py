"""
    SquidModel - Access squid services using the squid-py api
"""

import logging

from web3 import Web3

from squid_py.config import Config as SquidConfig
from squid_py.ocean import Ocean as SquidOcean
from squid_py.did import (
    did_to_id_bytes,
    DID,
)
from squid_py.keeper import Keeper

from squid_py.agreements.service_agreement_template import ServiceAgreementTemplate
from squid_py.agreements.service_agreement import ServiceAgreement
from squid_py.agreements.service_types import ServiceTypes
from squid_py.brizo.brizo_provider import BrizoProvider
from squid_py.keeper.web3_provider import Web3Provider

from squid_py.ddo.metadata import Metadata

from plecos import is_valid_dict_local


logger = logging.getLogger('starfish')
# from starfish import logger

# to keep the squid_model seperate, we will issue a seperate purchase exception just
# from this class

class SquidModelPurchaseError(Exception):
    """ Raised when a purchase event has failed to complete """


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

        # to get past codacy static method 'register_agent'
        self._keeper = Keeper.get_instance()

    def register_asset(self, metadata, account):
        """

        Register an asset with the agent storage server

        :param dict metadata: metadata to write to the storage server
        :param object account: squid account to register the asset
        """
        squid_ocean = self.get_squid_ocean(account)
        return squid_ocean.assets.create(metadata, account)

    def validate_metadata(self, metadata):
        """

        Validate the metadata with plesto

        :param dict metadata: metadata to validate
        :return: True if the metadata is valid
        :type: boolean

        """
        # fix codacy to stop making this a static function
        if self._ocean:
            return is_valid_dict_local(metadata)
        return False

    def read_asset(self, did):
        """

        Read the asset metadata(DDO) using the asset DID

        :param str did: DID of the asset to read.

        :return: DDO of the read asset or None if not found
        :type: dict or None

        """
        return self._squid_ocean.assets.resolve(did)

    def search_assets(self, text, sort=None, offset=100, page=1):
        """
        Search assets from the squid API.
        """
        ddo_list = self._squid_ocean.assets.search(text, sort, offset, page)
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
        return self._squid_ocean._keeper.service_agreement.get_template_owner(template_id)

    def register_service_agreement_template(self, template_id, account):
        """
        Try to register service level agreement template using an account

        :param template_id: template id to use to register
        :param account: account to register for
        :return: The template registered
        """
        template = ServiceAgreementTemplate.from_json_file(get_sla_template_path())
        template = register_service_agreement_template(
            self._squid_ocean._keeper.service_agreement,
            account,
            template,
            self._squid_ocean._keeper.network_name
        )
        return template

    def purchase_asset(self, ddo, account):
        """
        Purchase an asset with the agent storage server
        :param dict ddo: ddo of the asset
        :param object account: squid account unlocked and has sufficient funds to buy this asset

        :return: service_agreement_id of the purchase or None if no purchase could be made
        """
        squid_ocean = self.get_squid_ocean(account)
        service_agreement_id = None
        service_agreement = SquidModel.get_service_agreement_from_ddo(ddo)
        if service_agreement:
            service_agreement_id = squid_ocean.assets.order(ddo.did, service_agreement.sa_definition_id, account, auto_consume=False)

        return service_agreement_id

    def purchase_wait_for_completion(self, purchase_id, timeoutSeconds):
        """

        Wait for a purchase to complete

        """
        event = self._keeper.escrow_access_secretstore_template.subscribe_agreement_created(
            purchase_id,
            timeoutSeconds,
            SquidModel.log_event(self._keeper.escrow_access_secretstore_template.AGREEMENT_CREATED_EVENT),
            (),
            wait=True
        )
        if not event:
            raise SquidModelPurchaseError('no event for EscrowAccessSecretStoreTemplate.AgreementCreated')

        event = self._keeper.lock_reward_condition.subscribe_condition_fulfilled(
            purchase_id,
            timeoutSeconds,
            SquidModel.log_event(self._keeper.lock_reward_condition.FULFILLED_EVENT),
            (),
            wait=True
        )
        if not event:
            raise SquidModelPurchaseError('no event for LockRewardCondition.Fulfilled')

        event = self._keeper.escrow_reward_condition.subscribe_condition_fulfilled(
            purchase_id,
            timeoutSeconds,
            SquidModel.log_event(self._keeper.escrow_reward_condition.FULFILLED_EVENT),
            (),
            wait=True
        )
        if not event:
            raise SquidModelPurchaseError('no event for EscrowReward.Fulfilled')

        return True

    def purchase_operation(self, ddo, account):
        """
        Purchase an invoke operation
        :param dict ddo: ddo of the asset
        :param object account: squid account unlocked and has sufficient funds to buy this asset

        :return: service_agreement_id of the purchase or None if no purchase could be made
        """
        service_agreement_id = None
        service_agreement = SquidModel.get_service_agreement_from_ddo(ddo)
        agreements=self._squid_ocean.agreements
        did=ddo.did
        if service_agreement:
            logger.info(f'purchase invoke operation ')
            service_definition_id=service_agreement.sa_definition_id

            service_agreement_id,signature = agreements.prepare(ddo.did, service_definition_id, account)
            asset = agreements._asset_resolver.resolve(did)

            service_agreement = ServiceAgreement.from_ddo(service_definition_id, asset)
            service_def = asset.find_service_by_id(service_definition_id).as_dictionary()

            # Must approve token transfer for this purchase

            agreements._approve_token_transfer(service_agreement.get_price(), account)
            # subscribe to events related to this agreement_id before sending the request.
            logger.debug(f'Registering service agreement with id: {service_agreement_id}')

            register_service_agreement( agreements._config.storage_path,
                                        account,
                                        service_agreement_id,
                                        did,
                                        service_def,
                                        'consumer',
                                        service_agreement.sa_definition_id,
                                        service_agreement.get_price(),
                                        asset.encrypted_files,
                                        start_time=None
            )

            BrizoProvider.get_brizo().initialize_service_agreement(did,
                                                                   service_agreement_id,
                                                                   service_agreement.sa_definition_id,
                                                                   signature,
                                                                   account.address,
                                                                   service_agreement.purchase_endpoint)

        return service_agreement_id


    def consume_asset(self, ddo, service_agreement_id, account, download_path):
        """
        Conusmer the asset data, by completing the payment and later returning the data for the asset

        """
        squid_ocean = self.get_squid_ocean(account)
        service_agreement = SquidModel.get_service_agreement_from_ddo(ddo)
        if service_agreement:
            squid_ocean.assets.consume(service_agreement_id, ddo.did, service_agreement.sa_definition_id, account, download_path)

    def is_access_granted_for_asset(self, did, service_agreement_id, account):
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

        return self._squid_ocean.agreements.is_access_granted(service_agreement_id, did, account_address)

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
                'storage.path': self._storage_path
            }
        }
        if options:
            if 'parity_address' in options:
                data['keeper-contracts']['parity.address'] = options['parity_address']
            if 'parity_password' in options:
                data['keeper-contracts']['parity.password'] = options['parity_password']

        return data

    def get_account(self, address, password=None):
        """
        :return: sqiud account object if the address is found, else None
        :type: object or None
        """
        for account in self.accounts:
            if account.address == address:
                account.password=password
                return account

    def request_tokens(self, account, value):
        """
        Request some ocean tokens
        :param object account: squid account to request
        :param number value: amount of tokens to request
        :return: number of tokens requested and added to the account
        :type: number
        """
        return self._squid_ocean.accounts.request_tokens(account, value)

    def get_account_balance(self, account):
        """

        :param object account: squid account to get the balance for.
        :return: ethereum and ocean balance of the account
        :type: tuple(eth,ocn)
        """
        return self._squid_ocean.accounts.balance(account)

    def create_account(self, password):
        """

        :param str password: password of the new account
        :return: None or squid account of the new account.
        :type: object or None

        """
        local_account = Web3Provider.get_web3().eth.account.create(password)
        # need to reload squid again so that it sees the new account
        # TODO: does not work at the moment, new account does not get
        # shown in squid
        logger.info(f'new account address {local_account.address}')
        self._squid_ocean = self.get_squid_ocean()
        account_list = Web3Provider.get_web3().eth.accounts
        logger.info(f'current account list {account_list}')
        account = self.get_account(local_account.address, password)
        logger.info(f'found account {account}')
        return local_account.address

    def register_ddo(self, did, ddo_text, account):
        """register a ddo object on the block chain for this agent"""
        # register/update the did->ddo to the block chain

        checksum = Web3.toBytes(Web3.sha3(ddo_text.encode()))
        # did_bytes = did_to_id_bytes(did)
        receipt = self._squid_ocean._keeper.did_registry.register(did, checksum, ddo_text, account._squid_account)

        # transaction = self._squid_ocean._keeper.did_registry._register_attribute(did_id, checksum, ddo_text, account, [])
        # receipt = self._squid_ocean._keeper.did_registry.get_tx_receipt(transaction)
        return receipt

    def resolve_did(self, did):
        """resolve a DID to a given DDO, return the DDO if found"""

        did_bytes = did_to_id_bytes(did)
        data = self._keeper.did_registry.get_registered_attribute(did_bytes)
        if data:
            return data['value']
        return None

    @property
    def accounts(self):
        return self._squid_ocean.accounts.list()

    @property
    def aquarius_url(self):
        return self._aquarius_url

    @property
    def brizo_url(self):
        return self._brizo_url

    def get_squid_ocean(self, account=None):
        """

        Return an instance of squid for an account

        """

        options = {}
        if account:
            options['parity_address'] = account.address
            options['parity_password'] = account.password

        config_params = self._as_config_dict(options)
        config = SquidConfig(options_dict=config_params)
        return SquidOcean(config)

    @staticmethod
    def get_service_agreement_from_ddo(ddo):
        """
        return the service agreement definition for this asset
        """
        service_agreement = None
        if ddo:
            service = ddo.get_service(service_type=ServiceTypes.ASSET_ACCESS)
            assert ServiceAgreement.SERVICE_DEFINITION_ID in service.as_dictionary()
            service_agreement = ServiceAgreement.from_service_dict(service.as_dictionary())
        return service_agreement

    @staticmethod
    def get_default_metadata():
        return Metadata.get_example()

    @staticmethod
    def log_event(event_name):
        def _process_event(event):
            logging.debug(f'Received event {event_name}: {event}')
        return _process_event

    @staticmethod
    def generate_did():
        return DID.did()
