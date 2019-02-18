import os
import logging
import json

from unittest.mock import Mock
from squid_py import ConfigProvider
from squid_py.brizo.brizo import Brizo

from starfish.logging import setup_logging

setup_logging(level=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("web3").setLevel(logging.WARNING)


class BrizoMock(object):
    def __init__(self, ocean_instance=None, account=None):
        self.ocean_instance = ocean_instance
        """
        if not ocean_instance:
            from tests.resources.helper_functions import get_publisher_ocean_instance
            self.ocean_instance = get_publisher_ocean_instance(
                init_tokens=False, use_ss_mock=False, use_brizo_mock=False
            )
        """
        self.account = account
        """
        if not account:
            from tests.resources.helper_functions import get_publisher_account
            self.account = get_publisher_account(ConfigProvider.get_config())
        """
    def get(self, url, *args, **kwargs):
        response = Mock()
        response.data = b'good luck squiddo.'
        response.status_code = 200
        response.url = 'http://mock.url/filename.mock?blahblah'
        response.content = b'asset data goes here.'
        return response

    def post(self, url, data=None, **kwargs):
        response = Mock()
        logging.debug(f'mock post url {url}')
        if url.endswith('initialize'):
            payload = json.loads(data)
            did = payload['did']
            service_definition_id = payload['serviceDefinitionId']
            agreement_id = payload['serviceAgreementId']
            signature = payload['signature']
            consumer_address = payload['consumerAddress']
            self.ocean_instance.agreements.create(
                did,
                service_definition_id,
                agreement_id,
                signature,
                consumer_address,
                self.account
            )

            response.status_code = 201
        else:
            response.status_code = 404
        return response

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
                        destination_folder):
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
