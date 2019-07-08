import os
import logging
import json
import time

from unittest.mock import Mock
from eth_utils import add_0x_prefix

from squid_py import ConfigProvider
from squid_py.brizo.brizo import Brizo
from squid_py.did import id_to_did, did_to_id
from squid_py.agreements.service_agreement import ServiceAgreement
from squid_py.agreements.service_types import ServiceTypes
from squid_py.keeper.web3_provider import Web3Provider
from squid_py.keeper import Keeper
from squid_py.keeper.events_manager import EventsManager
# from squid_py.agreements.manager import AgreementsManager

logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('web3').setLevel(logging.WARNING)

logger = logging.getLogger('test.mocks.brizo_mock')

class BrizoMock(object):

    def __init__(self, ocean_instance=None, account=None):
        self._ocean_instance = ocean_instance
        self._is_event_subscribed = False
        self._ddo_records = {}
    """
    def subscribe(self, ocean, account, did, ddo):
        self._account = account
        model = ocean.get_squid_model()
        self._ocean_instance = model.get_squid_ocean(account)
        self._is_event_subscribed = False

        self._ddo_records[did] = ddo
        events_manager = EventsManager.get_instance(Keeper.get_instance())
        events_manager.stop_all_listeners()
        time.sleep(1)
        events_manager.agreement_listener._event_filters = dict()
        self._ocean_instance.agreements.subscribe_events(
            self._account.address,
            self._handle_agreement_created,
        )
        # at the moment we need to do this sleep or the event handle below
        # is not called. Not sure why?
        time.sleep(1)

    def _handle_agreement_created(self, event, *_):
#        print('_handle_agreement_created ', event)
        try:
            if not event or not event.args:
                print('no handle created')
                return

            self._is_event_subscribed = True
            print(f'Start handle_agreement_created: event_args={event.args}')
            config = ConfigProvider.get_config()
            provider_account = self._account
            assert provider_account.address == event.args['_accessProvider']

            did = id_to_did(event.args['_did'])
            agreement_id = Web3Provider.get_web3().toHex(event.args['_agreementId'])

            ddo = self._ddo_records[did]
            # calling the resolve calls the squid_py.aquarius module.
            # The module calls a http request session object created outside of this thread
            # and so can cause crashes
            #ddo = ocean.assets.resolve(did)
            sa = ServiceAgreement.from_ddo(ServiceTypes.ASSET_ACCESS, ddo)

            condition_ids = sa.generate_agreement_condition_ids(
                agreement_id=agreement_id,
                asset_id=add_0x_prefix(did_to_id(did)),
                consumer_address=event.args['_accessConsumer'],
                publisher_address=ddo.publisher,
                keeper=Keeper.get_instance())

            events_manager = EventsManager.get_instance(Keeper.get_instance())
            agreements_manager = AgreementsManager(
                config,
                Keeper.get_instance(),
                events_manager,
                config.storage_path
            )
            agreements_manager.register_publisher(
                event.args['_accessConsumer'],
                agreement_id,
                did,
                sa,
                sa.service_definition_id,
                sa.get_price(),
                provider_account,
                condition_ids
            )
            print(f'handle_agreement_created() -- done registering event listeners.')
        except e as Exception:
            message = f'error with exception {e}'
            print(message)
            logger.error(message)
            raise

    @property
    def is_event_subscribed(self):
        return self._is_event_subscribed

    """

    def initialize_service_agreement(did, agreement_id, service_definition_id,
                                     signature, account_address, purchase_endpoint):
        print(f'BrizoMock.initialize_service_agreement: purchase_endpoint={purchase_endpoint}')
        self._ocean_instance.agreements.create(
            did,
            service_definition_id,
            agreement_id,
            signature,
            account_address,
            self._account
        )
        return True

    @staticmethod
    def consume_service(service_agreement_id, service_endpoint, account_address, files,
                        destination_folder, *_, **__):
        for f in files:
            with open(os.path.join(destination_folder, os.path.basename(f['url'])), 'w') as of:
                of.write(f'mock data {service_agreement_id}.{service_endpoint}.{account_address}')

    @staticmethod
    def invoke_service(service_agreement_id, service_endpoint, account_address, invoke_payload):
        """
        Call the Koi endpoint to get access to the different files that form the asset.

        :param service_agreement_id: Service Agreement Id, str
        :param service_endpoint: Url to consume, str
        :param account_address: ethereum address of the consumer signing this agreement, hex-str
        :param files: List containing the files to be consumed, list
        :param destination_folder: Path, str
        :return:
        """
        logger.info(f'invoke endpoint with this url: {service_endpoint}')

        return invoke_payload['params']

    @staticmethod
    def get_brizo_url(config):
        return Brizo.get_brizo_url(config)


    @staticmethod
    def get_purchase_endpoint(config):
        return f'{Brizo.get_brizo_url(config)}/services/access/initialize'

    @staticmethod
    def get_service_endpoint(config):
        return f'{Brizo.get_brizo_url(config)}/services/consume'
