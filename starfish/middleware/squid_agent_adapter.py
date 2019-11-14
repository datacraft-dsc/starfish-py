"""
    SquidAgentAdapter - Access squid services using the squid-py api
"""

import logging
import time
import json

from web3 import Web3

from ocean_keeper.account import Account as SquidAccount

from squid_py.config_provider import ConfigProvider
from squid_py.config import Config as SquidConfig
from squid_py.ocean import Ocean as SquidOcean
from ocean_utils.did import (
    did_to_id_bytes,
    did_to_id,
    DID,
)
from squid_py.ocean.keeper import SquidKeeper

from ocean_utils.agreements.service_agreement import ServiceAgreement
from ocean_utils.agreements.service_types import ServiceTypes
from squid_py.brizo.brizo_provider import BrizoProvider
from ocean_keeper.web3_provider import Web3Provider
from squid_py.ocean.ocean_tokens import OceanTokens

from ocean_utils.ddo.metadata import Metadata
from ocean_keeper.agreements.agreement_manager import AgreementStoreManager
from plecos import is_valid_dict_local, validate_dict_local

from starfish.middleware.starfish_events_manager import StarfishEventsManager


logger = logging.getLogger('starfish.squid_agent_adapter')
# from starfish import logger

# to keep the squid_agent_adapter seperate, we will issue a seperate purchase exception just
# from this class

class SquidAgentAdapterPurchaseError(Exception):
    """ Raised when a purchase event has failed to complete """


class AgreementStoreManagerExtra(AgreementStoreManager):
    def get_agreement_ids_for_did(self, did):
        return self.contract_concise.getAgreementIdsForDID(did)

class SquidAgentAdapter():


    def __init__(self, ocean, options=None):
        """init a standard ocean object"""
        self._ocean = ocean
        self._squid_ocean = None

        if not isinstance(options, dict):
            options = {}

        self._aquarius_url = options.get('aquarius_url', 'http://localhost:5000')
        self._brizo_url = options.get('brizo_url', 'http://localhost:8030')
        self._secret_store_url = options.get('secret_store_url', 'http://localhost:12001')
        self._storage_path = options.get('storage_path', 'squid_py.db')
        self._parity_url = options.get('parity_url', self._ocean.keeper_url)


        # clear out any old connections to a different network
        # this means removing the static web3 connection in squid
        Web3Provider._web3 = None

        # make sure we have a instance of squid ocean created before starting
        self.get_squid_ocean()

        # to get past codacy static method 'register_agent'
        self._keeper = SquidKeeper.get_instance()

    def register_asset(
            self, metadata, account,
            service_descriptors=None, providers=None, use_secret_store=True):
        """

        Register an asset with the agent storage server

        :param dict metadata: metadata to write to the storage server
        :param object account: squid account to register the asset
        :param dict options: options to pass to the squid asset create function
        """
        squid_ocean = self.get_squid_ocean(account)
        return squid_ocean.assets.create(
            metadata,
            account,
            service_descriptors,
            providers,
            use_secret_store
            )

    def validate_metadata(self, metadata):
        """

        Validate the metadata with plesto

        :param dict metadata: metadata to validate
        :return: True if the metadata is valid
        :type: boolean

        """
        if self._ocean:
            if is_valid_dict_local(metadata):
                return True
            else:
                validator = validate_dict_local(metadata)
                print(validator)
        return False

    def read_asset(self, did):
        """

        Read the asset metadata(DDO) using the asset DID

        :param str did: DID of the asset to read.

        :return: DDO of the read asset or None if not found
        :type: dict or None

        """
        squid_ocean = self.get_squid_ocean()
        return squid_ocean.assets.resolve(did)

    def search_assets(self, text, sort=None, offset=100, page=1):
        """
        Search assets from the squid API.
        """
        squid_ocean = self.get_squid_ocean()
        if isinstance(text, str):
            ddo_list = squid_ocean.assets.search(text, sort, offset, page)
        elif isinstance(text, dict):
            ddo_list = squid_ocean.assets.query({'query': text}, sort, offset, page)
        else:
            ddo_list = None
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
        return self._keeper.service_agreement.get_template_owner(template_id)

    def register_service_agreement_template(self, template_id, account):
        """
        Try to register service level agreement template using an account

        :param template_id: template id to use to register
        :param account: account to register for
        :return: The template registered


        # template = ServiceAgreementTemplate.from_json_file(get_sla_template_path())
        template = register_service_agreement_template(
            self._keeper.service_agreement,
            account,
            template,
            self._keeper.network_name
        )
        return template
        """
        return None

    @staticmethod
    def get_asset_purchase_ids(did):
        """
        Return a list of purchase id's that have been issued for an asset did
        """
        result = []
        manager = AgreementStoreManagerExtra.get_instance()
        id_list = manager.get_agreement_ids_for_did(did_to_id(did))
        for value in id_list:
            result.append(Web3.toHex(value))
        return result

    def purchase_asset(self, ddo, account):
        """
        Purchase an asset with the agent storage server
        :param dict ddo: ddo of the asset
        :param object account: squid account unlocked and has sufficient funds to buy this asset

        :return: service_agreement_id of the purchase or None if no purchase could be made
        """
        squid_ocean = self.get_squid_ocean(account)

        service_agreement_id = None
        service_agreement = SquidAgentAdapter.get_service_agreement_from_ddo(ddo)
        if service_agreement:
            service_agreement_id = squid_ocean.assets.order(
                ddo.did,
                service_agreement.sa_definition_id,
                account,
                auto_consume=False
            )
        return service_agreement_id

    def purchase_wait_for_completion(self, did, address, purchase_id, timeout_seconds):
        """

        Wait for a purchase to complete

        """

        event = self._keeper.escrow_access_secretstore_template.subscribe_agreement_created(
            purchase_id,
            timeout_seconds,
            SquidAgentAdapter.log_event(self._keeper.escrow_access_secretstore_template.AGREEMENT_CREATED_EVENT),
            (),
            wait=True
        )
        if not event:
            raise SquidAgentAdapterPurchaseError('no event for EscrowAccessSecretStoreTemplate.AgreementCreated')

        event = self._keeper.lock_reward_condition.subscribe_condition_fulfilled(
            purchase_id,
            timeout_seconds,
            SquidAgentAdapter.log_event(self._keeper.lock_reward_condition.FULFILLED_EVENT),
            (),
            wait=True
        )
        if not event:
            raise SquidAgentAdapterPurchaseError('no event for LockRewardCondition.Fulfilled')

        timeout_time = time.time() + timeout_seconds
        while self.is_access_granted_for_asset(did, address, purchase_id) is not True and timeout_time > time.time():
            time.sleep(1)

        return self.is_access_granted_for_asset(did, address, purchase_id)

    def purchase_operation(self, ddo, account):
        """
        Purchase an invoke operation
        :param dict ddo: ddo of the asset
        :param object account: squid account unlocked and has sufficient funds to buy this asset

        :return: service_agreement_id of the purchase or None if no purchase could be made
        """
        squid_ocean = self.get_squid_ocean()

        service_agreement_id = None
        service_agreement = SquidAgentAdapter.get_service_agreement_from_ddo(ddo)
        agreements = squid_ocean.agreements
        did = ddo.did
        if service_agreement:
            logger.info(f'purchase invoke operation ')
            service_definition_id = service_agreement.sa_definition_id

            service_agreement_id, signature = agreements.prepare(ddo.did, service_definition_id, account)
            asset = agreements._asset_resolver.resolve(did)

            service_agreement = ServiceAgreement.from_ddo(service_definition_id, asset)
            # service_def = asset.find_service_by_id(service_definition_id).as_dictionary()

            # Must approve token transfer for this purchase

            agreements._approve_token_transfer(service_agreement.get_price(), account)
            # subscribe to events related to this agreement_id before sending the request.
            logger.debug(f'Registering service agreement with id: {service_agreement_id}')

            BrizoProvider.get_brizo().initialize_service_agreement(did,
                                                                   service_agreement_id,
                                                                   service_agreement.sa_definition_id,
                                                                   signature,
                                                                   account.address,
                                                                   service_agreement.purchase_endpoint)

        return service_agreement_id


    def consume_asset(self, ddo, account, service_agreement_id):
        """
        Conusmer the asset data, by completing the payment and later returning the data for the asset

        """
        result = None
        squid_ocean = self.get_squid_ocean(account)
        service_agreement = SquidAgentAdapter.get_service_agreement_from_ddo(ddo)
        if service_agreement:
            result = json.loads(squid_ocean.secret_store.decrypt(
                    ddo.asset_id,
                    ddo.metadata['base']['encryptedFiles'],
                    account
            ))

#        squid_ocean.assets.consume(service_agreement_id, ddo.did, service_agreement.sa_definition_id, account, download_path)
        return result

    def is_access_granted_for_asset(self, did, account, agreement_id):
        """
        Return true if we have access to the asset's data using the service_agreement_id and account used
        to purchase this asset
        """
        squid_ocean = self.get_squid_ocean()

        account_address = None
        if isinstance(account, object):
            account_address = account.address
        elif isinstance(account, str):
            account_address = account
        else:
            raise TypeError(f'You need to pass an account object or account address')

        return squid_ocean.agreements.is_access_granted(agreement_id, did, account_address)

    def get_purchase_address(self, agreement_id):
        return self._keeper.escrow_access_secretstore_template.get_agreement_consumer(agreement_id)

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
                'downloads.path': '',
            }
        }
        if options:
            if 'parity_address' in options:
                data['keeper-contracts']['parity.address'] = options['parity_address']
            if 'parity_password' in options:
                data['keeper-contracts']['parity.password'] = options['parity_password']
            if 'parity_keyfile' in options:
                data['keeper-contracts']['parity.keyfile'] = options['parity_keyfile']

        return data

    @staticmethod
    def get_account(address, password, keyfile):
        """
        :return: Squid Account object, based on it's address, password and JSON keyfile
        :type: object or None
        """
        return SquidAccount(address, password, keyfile)

    def request_tokens(self, account, value):
        """
        Request some ocean tokens
        :param object account: squid account to request
        :param int value: amount of tokens to request
        :return: number of tokens requested and added to the account
        :type: number
        """
        squid_ocean = self.get_squid_ocean()
        return squid_ocean.accounts.request_tokens(value, account)

    def get_account_balance(self, account):
        """

        :param object account: squid account to get the balance for.
        :return: ethereum and ocean balance of the account
        :type: tuple(eth,ocn)
        """
        squid_ocean = self.get_squid_ocean()
        return squid_ocean.accounts.balance(account)

    @staticmethod
    def create_account_host(password):
        """

        Create a hosted account on the block chain node

        :param str password: password of the new account
        :return: None or squid account of the new account.
        :type: object or None

        """
        account_address = Web3Provider.get_web3().personal.newAccount(password)
        return account_address

    @staticmethod
    def transfer_ether(from_account, to_address, amount):
        tx_hash = Web3Provider.get_web3().personal.sendTransaction({
            'from': from_account.address,
            'to': to_address,
            'value': amount,
        }, from_account.password)
        return Web3Provider.get_web3().eth.waitForTransactionReceipt(tx_hash)

    def transfer_tokens(self, from_account, to_address, amount):
        tokens = OceanTokens(self._keeper.get_instance())
        return tokens.transfer(to_address, amount, from_account)

    def approve_tokens(self, spender_address, price, from_account):
        return self._keeper.token.token_approve(spender_address, price, from_account)

    def register_ddo(self, did, ddo_text, account):
        """register a ddo object on the block chain for this agent

        The account must be an agent_adapter acount
        """
        # register/update the did->ddo to the block chain
        squid_ocean = self.get_squid_ocean()
        checksum = Web3.toBytes(Web3.sha3(ddo_text.encode()))
        did_bytes = did_to_id_bytes(did)
        receipt = squid_ocean._keeper.did_registry.register(did_bytes, checksum, ddo_text, account)

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

    def start_agreement_events_monitor(self, account, callback=None):
        """ called by the publisher to watch payment request events for the published assets
        The account must be an agent_adapter account
        """
        squid_ocean = self.get_squid_ocean(account)

        events_manager = StarfishEventsManager.get_instance(
            squid_ocean._keeper, squid_ocean._config.storage_path, account)

        events_manager.start_agreement_events_monitor(callback)

    def stop_agreement_events_monitor(self, account=None):
        """ called by the publisher to watch payment request events for the published assets
        The account must be an agent_adapter account
        """
        squid_ocean = self.get_squid_ocean(account)

        events_manager = StarfishEventsManager.get_instance(
            squid_ocean._keeper, squid_ocean._config.storage_path, account)

        events_manager.stop_agreement_events_monitor()


    @property
    def accounts(self):
        squid_ocean = self.get_squid_ocean()
        return squid_ocean.accounts.list()

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
        if not self._squid_ocean:
            config_params = self._as_config_dict(options)
            config = SquidConfig(options_dict=config_params)
            ConfigProvider.set_config(config)
            self._squid_ocean = SquidOcean()
        return self._squid_ocean

    @staticmethod
    def get_service_agreement_from_ddo(ddo):
        """
        return the service agreement definition for this asset
        """
        service_agreement = None
        if ddo:
            service = ddo.get_service(service_type=ServiceTypes.ASSET_ACCESS)
            if ServiceAgreement.SERVICE_DEFINITION_ID not in service.as_dictionary():
                raise KeyError(f'cannot find services definition id {ServiceAgreement.SERVICE_DEFINITION_ID}')
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
