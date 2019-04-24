"""
    SurferModel - Model to access the Surfer Services
"""
import json
import requests
from web3 import Web3

from squid_py.did_resolver.did_resolver import DIDResolver
from squid_py.ddo.ddo import DDO

from starfish import logger

# default base URI for this version surfer
SURFER_BASE_URI = '/api/v1'

SUPPORTED_SERVICES = {
    'metadata': { 
        'type': 'Ocean.Meta.v1', 
        'uri': f'{SURFER_BASE_URI}/meta/data',
    },
    'storage': {
        'type': 'Ocean.Storage.v1',
        'uri': f'{SURFER_BASE_URI}/assets',
    },
    'invoke': {
        'type': 'Ocean.Invoke.v1',
        'uri': f'{SURFER_BASE_URI}/data',
    },
    'market': {
        'type': 'Ocean.Market.v1',
        'uri': f'{SURFER_BASE_URI}/market',
    },
    'trust': {
        'type': 'Ocean.Trust.v1',
        'uri': f'{SURFER_BASE_URI}/trust',
    },
    'auth': {
        'type': 'Ocean.Auth.v1',
        'uri': f'{SURFER_BASE_URI}/auth',
    },
}

class SurferModel():
    _http_client = requests

    def __init__(self, ocean, did=None, ddo=None, options=None):
        """init a standard ocan connection, with a given DID"""
        self._ocean = ocean
        self._did = did
        self._ddo = ddo
        if not options:
            options = {}

        self._headers = {'content-type': 'application/json'}
        authorization = options.get('authorization')
        if authorization: # this is an OAuth2 token
            self._headers['Authorization'] = f'token {authorization}'

    def register_asset(self, metadata):
        """
        Register an asset with the agent storage server
        :param metadata: metadata to write to the storage server

        :return: A dict of the following items
        [0] asset_id.
        [1] did of the asset.
        [2] metadata in text format, that was saved.

        :type: dict
        """
        result = None
        metadata_text = json.dumps(metadata)
        endpoint = self.get_endpoint('metadata')
        saved_asset_id = self.save_metadata(metadata_text, endpoint)
        result = {
                'asset_id': saved_asset_id,
                'metadata_text': metadata_text,
            }
        return result

    def save_metadata(self, metadata_text, endpoint):
        """save metadata to the agent server, using the asset_id and metadata"""
        url = endpoint
        logger.debug(f'metadata save url {url}')
        response = SurferModel._http_client.post(url, json=metadata_text, headers=self._headers)
        if response and response.status_code == requests.codes.ok:
            
            json = response.json()
            logger.warning(f'metadata asset response returned {json}')
            return json
        else:
            msg = f'metadata asset response failed: {response.status_code}'
            logger.error(msg)
            raise ValueError(msg)
        return None

    def create_listing(self,asset_id):
        endpoint = self.get_endpoint('market') + '/listings'
        metadata_text={'assetid':asset_id}
        response = SurferModel._http_client.post(endpoint, json=metadata_text, headers=self._headers)
        if response and response.status_code == requests.codes.ok:
            json = response.json()
            logger.warning('listing response returned: ' + str(json))
            return json
        else:
            msg = f'listing response failed: {response.status_code}'
            logger.error(msg)
            raise ValueError(msg)
        return None

    def read_asset(self, asset_id, endpoint):
        """read the metadata from a service agent using the asset_id"""

        result = None
        if endpoint:
            url = endpoint + '/' + asset_id
            logger.debug(f'metadata read url {url}')
            response = SurferModel._http_client.get(url, headers=self._headers)
            if response and response.status_code == requests.codes.ok:
                result = {
                    'asset_id': asset_id,
                    'metadata_text': response.content
                }
                # convert to str if bytes
                if isinstance(result['metadata_text'], bytes):
                    result['metadat_text'] = response.content.encode('utf-8')
            else:
                logger.warning(f'metadata asset read {asset_id} response returned {response}')
        return result

    def get_endpoint(self, name):
        """return the endpoint based on the name of the service"""
        if name in SUPPORTED_SERVICES:
            service = SUPPORTED_SERVICES[name]
            service_type = service['type']
        else:
            message = f'unknown surfer endpoint service: {name}'
            logger.error(message)
            raise ValueError(message)

        endpoint = None
        if self._ddo:
            service = self._ddo.get_service(service_type)
            if not service:
                message = f'unable to find surfer endpoint service type {service_type}'
                logger.error(message)
                raise ValueError(message)
            endpoint = service.endpoints.service
        if not endpoint:
            message = f'unable to find surfer endpoint for {name} = {service_type}'
            logger.error(message)
            raise ValueError(message)
        return endpoint

    @property
    def ddo(self):
        """return the DDO stored for this agent"""
        return self._ddo

    @property
    def did(self):
        """return the DID used for this agent"""
        return self._did

    @property
    def register_name(self):
        return self._register_name


    @staticmethod
    def is_metadata_valid(asset_id, metadata_text):
        """
        validate metadata, by calcualating the hash (asset_id) and compare this to the
        given asset_id, if both are equal then the metadata is valid
        :param asset_id: asset id to compare with
        :param metadata: dict of metadata to calculate the hash ( asset_id)
        :return bool True if metadata is valid for the asset_id provided
        """
        if metadata_text:
            # the calc asset_id from the metadata should be same as this asset_id
            metadata_id = SurferModel.get_asset_id_from_metadata(metadata_text)
            if metadata_id != asset_id:
                logger.debug(f'metdata does not match {metadata_id} != {asset_id}')
            return metadata_id == asset_id
        return False


    @staticmethod
    def get_asset_id_from_metadata(metadata_text):
        """
        return the asset_id calculated from the metadata
        :param metadata: dict of metadata to hash
        a 64 char hex string, which is the asset id
        :return 64 char hex string, with no leading '0x'
        """
        return Web3.toHex(Web3.sha3(metadata_text.encode()))[2:]

    @staticmethod
    def set_http_client(http_client):
        """Set the http client to something other than the default `requests`"""
        SurferModel._http_client = http_client

    @staticmethod
    def get_authorization_token(surfer_url, surfer_username, surfer_password):
        """Get a surfer authorization token (create one if needed).
        Throws exception on error."""
        token_url = surfer_url + SURFER_BASE_URI + '/auth/token'
        r = requests.get(token_url, auth=(surfer_username, surfer_password))
        token = None
        if r.status_code == 200:
            tokens = r.json()
            if len(tokens) > 0:
                token = tokens[-1]
            else: # need to create a token
                r = requests.post(token_url, auth=(surfer_username, surfer_password))
                if r.status_code == 200:
                    token = r.json()
                else:
                    msg = f'unable to create token, status {r.status_code}'
                    logger.error(msg)
                    raise ValueError(msg)
        else:
            msg = f'unable to get tokens, status {r.status_code}'
            logger.error(msg)
            raise ValueError(msg)
        logger.debug(f'using surfer token {token}')
        return token

    @staticmethod
    def get_supported_services(url):
        """
        Return a dict list of services available for this surfer
        in the format::
        
            {'name': service name, 'type': service_type, 'url': service endpoint url}
            
        """
        result = []
        for name, service in SUPPORTED_SERVICES.items():
            service_uri = service['uri']
            result.append({ 
                'name': name, 
                'type': service['type'],
                'url': f'{url}{service_uri}',
            })
        return result
