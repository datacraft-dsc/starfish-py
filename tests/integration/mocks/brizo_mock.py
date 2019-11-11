import os
import logging
import json
import time

from unittest.mock import Mock
from eth_utils import add_0x_prefix

from squid_py import ConfigProvider
from squid_py.brizo.brizo import Brizo
from ocean_utils.did import id_to_did, did_to_id
from ocean_utils.agreements.service_agreement import ServiceAgreement
from ocean_utils.agreements.service_types import ServiceTypes
# from squid_py.agreements.manager import AgreementsManager

logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('web3').setLevel(logging.WARNING)

logger = logging.getLogger('test.mocks.brizo_mock')

class BrizoMock(object):

    def __init__(self, ocean_instance=None, account=None):
        self._ocean_instance = ocean_instance
        self._is_event_subscribed = False
        self._ddo_records = {}

    def initialize_service_agreement(self, did, agreement_id, service_definition_id,
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
