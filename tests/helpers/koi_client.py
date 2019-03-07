"""koi client ."""
import sys,traceback
import json
import logging
import os

import requests
from tqdm import tqdm

from squid_py.agreements.service_agreement import ServiceAgreement
from squid_py.exceptions import OceanInitializeServiceAgreementError

from squid_py.brizo.brizo import Brizo
logger = logging.getLogger(__name__)


class KoiClient:
    """

    The main functions available are:
    - initialize_service_agreement
    - consume_service
    - run_compute_service (not implemented yet)

    """
    _http_client = requests

    @staticmethod
    def set_http_client(http_client):
        """Set the http client to something other than the default `requests`"""
        KoiClient._http_client = http_client

    @staticmethod
    def initialize_service_agreement(did, agreement_id, service_definition_id, signature,
                                     account_address,
                                     purchase_endpoint):
        """
        Send a request to the service provider (purchase_endpoint) to initialize the service
        agreement for the asset identified by `did`.

        :param did: str -- id of the asset includes the `did:op:` prefix
        :param agreement_id: hex str
        :param service_definition_id: str -- identifier of the service inside the asset DDO
        :param signature: hex str -- signed agreement hash
        :param account_address: hex str -- ethereum address of the consumer signing this agreement
        :param purchase_endpoint: str -- url of the service provider
        :return:
        """
        paymap={
            'asset-did': did,
            'service-agreement-id': agreement_id,
            'service-definition-id':service_definition_id,
            'signature': signature,
            'consumer-address': account_address
        }
        payload = json.dumps(paymap)
        logger.info(f' Koi client sending request to server {paymap}')
        response = KoiClient._http_client.post( purchase_endpoint, data=payload, headers={'content-type': 'application/json'})

        if response and hasattr(response, 'status_code'):
            if response.status_code != 201:
                msg = (f'Initialize service agreement failed at the purchaseEndpoint '
                       f'{purchase_endpoint}, reason {response.text}, status {response.status_code}'
                       )
                logger.error(msg)
                raise OceanInitializeServiceAgreementError(msg)

            logger.debug(
                f'Service agreement initialized successfully, service agreement id {agreement_id},'
                f' purchaseEndpoint {purchase_endpoint}')
            return True

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
        #TODO remove this hardcoding
        service_endpoint='http://localhost:8031/api/v1/brizo/services/invoke'
        logger.info(f'invoke endpoint with this url: {service_endpoint}')
        payload=json.dumps({'operationSAInfo':{'consumer-address': account_address, 'service-agreement-id': service_agreement_id}, 
            'payload':invoke_payload})
        response = KoiClient._http_client.post( service_endpoint, data=payload, headers={'content-type': 'application/json'}) 
            
        logger.info(f'invoke endpoint response : {response}')

        if response.status_code == 200: 
            logger.info(f'response successful') 
        else: 
            logger.warning(f'consume failed: {response.reason}')
        return json.loads(response.text)

    @staticmethod
    def get_brizo_url(config):
        """
        Return the Brizo component url.

        :param config: Config
        :return: Url, str
        """
        brizo_url = 'http://localhost:8031'
        if config.has_option('resources', 'brizo.url'):
            brizo_url = config.get('resources', 'brizo.url') or brizo_url

        brizo_path = '/api/v1/brizo'
        return f'{brizo_url}{brizo_path}'

    @staticmethod
    def get_purchase_endpoint(config):
        """
        Return the endpoint to purchase the asset.

        :param config:Config
        :return: Url, str
        """
        return f'{Brizo.get_brizo_url(config)}/services/access/initialize'

    @staticmethod
    def get_service_endpoint(config):
        """
        Return the url to consume the asset.

        :param config: Config
        :return: Url, str
        """
        return f'{Brizo.get_brizo_url(config)}/services/invoke'
