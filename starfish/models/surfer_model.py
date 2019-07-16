"""
    SurferModel - Model to access the Surfer Services
"""
import io
import json
import requests
from web3 import Web3

from squid_py.did_resolver.did_resolver import DIDResolver

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
        'uri': f'{SURFER_BASE_URI}/invoke',
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

INVOKE_SYNC_METHOD = '/invoke'
INVOKE_ASYNC_METHOD = '/invokeasync'
INVOKE_JOB_METHOD = '/jobs'

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
        saved_asset_id = self.save_metadata(metadata)
        result = {
                'asset_id': saved_asset_id,
                'metadata': metadata,
            }
        return result

    def save_metadata(self, metadata):
        """save metadata to the agent server, using the asset_id and metadata"""
        url = self.get_endpoint('metadata')
        logger.debug(f'metadata save url {url}')
        response = SurferModel._http_client.post(url, json=metadata, headers=self._headers)
        if response and response.status_code == requests.codes.ok:

            data = response.json()
            logger.debug(f'metadata asset response returned {data}')
            return data
        else:
            msg = f'metadata asset response failed: {response.status_code}'
            logger.error(msg)
            raise ValueError(msg)
        return None

    def create_listing(self, asset_id, listing_data):
        endpoint = self.get_endpoint('market')
        url = f'{endpoint}/listings'
        data = {
            'assetid': asset_id,
            'info': listing_data,
        }
        response = SurferModel._http_client.post(url, json=data, headers=self._headers)
        if response and response.status_code == requests.codes.ok:
            data = response.json()
            logger.debug('listing response returned: ' + str(data))
            return data
        else:
            msg = f'listing response failed: {response.status_code} {response.text}'
            logger.error(msg)
            raise ValueError(msg)
        return None

    def download_asset(self, url):
        response = SurferModel._http_client.get(url, headers=self._headers)
        if response and response.status_code == requests.codes.ok:
            data = response.content
            return data
        else:
            msg = f'GET assets response failed: {response.status_code} {response.text}'
            logger.error(msg)
            raise ValueError(msg)
        return None

    def get_asset_store_url(self, asset_id):
        endpoint = self.get_endpoint('storage')
        url = f'{endpoint}/{asset_id}'
        return url

    def get_listing(self, listing_id):
        endpoint = self.get_endpoint('market')
        url = f'{endpoint}/listings/{listing_id}'
        response = SurferModel._http_client.get(url, headers=self._headers)
        if response and response.status_code == requests.codes.ok:
            data = response.json()
            return data
        else:
            msg = f'GET listings response failed: {response.status_code}'
            logger.error(msg)
            raise ValueError(msg)
        return None

    def get_listings(self):
        endpoint = self.get_endpoint('market')
        url = f'{endpoint}/listings'
        response = SurferModel._http_client.get(url, headers=self._headers)
        if response and response.status_code == requests.codes.ok:
            data = response.json()
            return data
        else:
            msg = f'GET listings response failed: {response.status_code}'
            logger.error(msg)
            raise ValueError(msg)
        return None

    def update_listing(self, listing_id, data):
        endpoint = self.get_endpoint('market')
        url = f'{endpoint}/listings/{listing_id}'
        response = SurferModel._http_client.put(url, json=data, headers=self._headers)
        if response and response.status_code == requests.codes.ok:
            return True
        else:
            msg = f'PUT listings response failed: {response.status_code}'
            logger.error(msg)
            raise ValueError(msg)
        return None

    def upload_asset_data(self, url, asset_id, data):
        logger.debug(f'uploading data to {url}')
        data_bytes = data
        if not isinstance(data_bytes, bytes):
            data_bytes = data.encode()

        files = { 'file':  ( asset_id, io.BytesIO(data_bytes), 'application/octet-stream') }
        headers = {
            'Authorization': self._headers['Authorization']
        }
        response = SurferModel._http_client.post(url, files=files, headers=headers)
        if response and (response.status_code == requests.codes.ok or response.status_code == requests.codes.created):
            return True
        else:
            msg = f'upload asset response failed: {response.status_code}'
            logger.error(msg)
            raise ValueError(msg)
        return None

    def read_metadata(self, asset_id):
        """read the metadata from a service agent using the asset_id"""

        result = None
        endpoint = self.get_endpoint('metadata')
        url = f'{endpoint}/{asset_id}'
        logger.debug(f'metadata read url {url}')
        response = SurferModel._http_client.get(url, headers=self._headers)
        if response and response.status_code == requests.codes.ok:
            result = {
                'asset_id': asset_id,
                'metadata_text': response.content
            }
            # convert to str if bytes
            if isinstance(result['metadata_text'], bytes):
                result['metadata_text'] = response.content.decode('utf-8')
        else:
            logger.warning(f'metadata asset read {asset_id} response returned {response}')
        return result

    def purchase_asset(self, purchase):
        """record purchase"""
        url = self.get_endpoint('market') + '/purchases'
        logger.debug(f'market url for purchases {url}')
        response = SurferModel._http_client.post(url, json=purchase, headers=self._headers)
        if response and response.status_code == requests.codes.ok:

            json = response.json()
            logger.debug(f'purchase response returned {json}')
            return json
        else:
            msg = f'purchase response failed: {response.status_code}'
            logger.error(msg)
            # NOTE surfer may return error information in additon to a 500
            if response:
                json = response.json()
                logger.error(f'purchase response returned {json}')
            raise ValueError(msg)
        return None


    def invoke(self, asset_id, params, is_async=False):
        """

        call the invoke based on the asset_id without leading 0x
        """
        endpoint = self.get_endpoint('invoke')

        if is_async:
            url = f'{endpoint}{INVOKE_ASYNC_METHOD}/{asset_id}'
        else:
            url = f'{endpoint}{INVOKE_SYNC_METHOD}/{asset_id}'
        print(f'request {url}')
        response = SurferModel._http_client.post(url, json=params, headers=self._headers)
        if response and (response.status_code == requests.codes.ok or response.status_code == 201):
            json = response.json()
            logger.debug('invoke response returned: ' + str(json))
            return json
        else:
            msg = f'invoke response failed: {response.status_code} {response.text}'
            logger.error(msg)
            raise ValueError(msg)
        return None

    def get_job(self, job_id):
        endpoint = self.get_endpoint('invoke')
        url = f'{endpoint}{INVOKE_JOB_METHOD}/{job_id}'
        response = SurferModel._http_client.get(url, headers=self._headers)
        if response and response.status_code == requests.codes.ok:
            data = response.json()
            return data
        else:
            msg = f'GET job response failed: {response.status_code}'
            logger.error(msg)
            raise ValueError(msg)
        return None


    def get_endpoint(self, name):
        """return the endpoint based on the name of the service or service type"""
        supported_service = SurferModel.find_supported_service(name)
        if supported_service is None:
            message = f'unknown surfer endpoint service name or type: {name}'
            logger.error(message)
            raise ValueError(message)

        service_type = supported_service['type']
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
    def find_supported_service(search_name_type):
        """ return the supported service record if the name or service type is found
        else return None """
        for name, service in SUPPORTED_SERVICES.items():
            if service['type'] == search_name_type:
                return service
            if name == search_name_type:
                return service
        return None

    @staticmethod
    def generate_service_endpoints(url):
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
