import os
import logging
import json

from unittest.mock import Mock
from eth_utils import add_0x_prefix

from squid_py import ConfigProvider
from squid_py.brizo.brizo import Brizo
from squid_py.did import id_to_did, did_to_id
from squid_py.agreements.register_service_agreement import register_service_agreement_publisher
from squid_py.agreements.service_agreement import ServiceAgreement
from squid_py.agreements.service_types import ServiceTypes
from squid_py.keeper.web3_provider import Web3Provider
from squid_py.keeper import Keeper

from starfish.logging import setup_logging

setup_logging(level=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("web3").setLevel(logging.WARNING)

class BrizoMock(object):
    publisher_account = None
    ocean_instance = None

    def __init__(self, ocean_instance=None, account=None):
        self.ocean_instance = ocean_instance
        if not self.ocean_instance:
            self.ocean_instance = BrizoMock.ocean_instance

        self.account = account
        if not self.account:
            self.account = BrizoMock.publisher_account

        self.ocean_instance.agreements.subscribe_events(
            self.account.address,
            self._handle_agreement_created
        )


    def _handle_agreement_created(self, event, *_):
#        print('_handle_agreement_created ', event)
        if not event or not event.args:
            return

        print(f'Start handle_agreement_created: event_args={event.args}')
        config = ConfigProvider.get_config()
        ocean = self.ocean_instance
        provider_account = self.account
        assert provider_account.address == event.args['_accessProvider']

        did = id_to_did(event.args['_did'])
        agreement_id = Web3Provider.get_web3().toHex(event.args['_agreementId'])

        ddo = ocean.assets.resolve(did)
        sa = ServiceAgreement.from_ddo(ServiceTypes.ASSET_ACCESS, ddo)

        condition_ids = sa.generate_agreement_condition_ids(
            agreement_id=agreement_id,
            asset_id=add_0x_prefix(did_to_id(did)),
            consumer_address=event.args['_accessConsumer'],
            publisher_address=ddo.publisher,
            keeper=Keeper.get_instance())

        register_service_agreement_publisher(
            config.storage_path,
            event.args['_accessConsumer'],
            agreement_id,
            did,
            sa,
            sa.service_definition_id,
            sa.get_price(),
            provider_account,
            condition_ids
        )
        # print(f'handle_agreement_created() -- done registering event listeners.')

    def initialize_service_agreement(self, did, agreement_id, service_definition_id,
                                     signature, account_address, purchase_endpoint):
        print(f'BrizoMock.initialize_service_agreement: purchase_endpoint={purchase_endpoint}')
        self.ocean_instance.agreements.create(
            did,
            service_definition_id,
            agreement_id,
            signature,
            account_address,
            self.account
        )
        return True

    @staticmethod
    def consume_service(service_agreement_id, service_endpoint, account_address, files,
                        destination_folder, *_, **__):
        for f in files:
            with open(os.path.join(destination_folder, os.path.basename(f['url'])), 'w') as of:
                of.write(f'mock data {service_agreement_id}.{service_endpoint}.{account_address}')

    @staticmethod
    def get_brizo_url(config):
        return Brizo.get_brizo_url(config)


    @staticmethod
    def get_purchase_endpoint(config):
        return f'{Brizo.get_brizo_url(config)}/services/access/initialize'

    @staticmethod
    def get_service_endpoint(config):
        return f'{Brizo.get_brizo_url(config)}/services/consume'
