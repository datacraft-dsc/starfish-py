"""
    SuferModel - Model to access the Sufer Service
"""
import json
import requests
from web3 import Web3

from squid_py.did_resolver.did_resolver import DIDResolver
from squid_py.ddo.ddo import DDO

from starfish import logger

# service endpoint type name to use for this agent
SURFER_AGENT_ENDPOINT_NAME = 'metadata-storage'
SURFER_BASE_URI = '/api/v1/meta/data'

class SurferModel():
    _http_client = requests

    def __init__(self, ocean, did=None, ddo=None, options=None):
        """init a standard ocan connection, with a given DID"""
        self._ocean = ocean

        if options is None:
            options = {}


        self._headers = {'content-type': 'application/json'}
        if options.get('authorization'):
            self._headers['Authorization'] = f'Basic {authorization}'

        if did is None or isinstance(did, str):
            self._did = did
        else:
            raise ValueError('did must be a type string')
        
        if ddo is None or isinstance(ddo, DDO) or isinstance(ddo, dict):
            self._ddo = ddo
        else:
            raise ValueEror('ddo must be a DOD object or type dict')
            
        # if DID then try to load in the linked DDO
        if self._did and not self._ddo:
            self._ddo = self._resolve_did_to_ddo(self._did)

    def register_asset(self, metadata):
        """
        Register an asset with the agent storage server
        :param metadata: metadata to write to the storage server

        """
        result = None
        metadata_text = json.dumps(metadata)
        asset_id = SurferModel.get_asset_id_from_metadata(metadata_text)
        endpoint = self._get_endpoint(SURFER_AGENT_ENDPOINT_NAME)
        saved_asset_id = self.save(asset_id, metadata_text, endpoint)
        if asset_id == saved_asset_id:
            result = {
                'asset_id': asset_id,
                'did': f'{self._did}/{asset_id}',
                'metadata_text': metadata_text,
            }
        return result

    def save(self, asset_id, metadata_text, endpoint):
        """save metadata to the agent server, using the asset_id and metadata"""
        url = endpoint + SURFER_BASE_URI + '/' + asset_id
        logger.debug(f'metadata save url {url}')
        response = SurferModel._http_client.put(url, data=metadata_text, headers=self._headers)
        if response and response.status_code == requests.codes.ok:
            if response.content == asset_id:
                return asset_id
            logger.warning(f'on asset save ( {asset_id} ) surfer returned an invalid asset id ({respones.content})')
            return None
        logger.warning(f'metadata asset save {asset_id} response returned {response}')
        return None

    def read_asset(self, asset_id):
        """read the metadata from a service agent using the asset_id"""
        result = None
        endpoint = self._get_endpoint(SURFER_AGENT_ENDPOINT_NAME)
        if endpoint:
            url = endpoint + SURFER_BASE_URI + '/' + asset_id
            logger.debug(f'metadata read url {url}')
            response = SurferModel._http_client.get(url, headers=self._headers)
            if response and response.status_code == requests.codes.ok:
                result = {
                    'asset_id': asset_id,
                    'did': f'{self._did}/{asset_id}',
                    'metadata_text': response.content.decode('utf-8')
                }
            else:
                logger.warning(f'metadata asset read {asset_id} response returned {response}')
        return result

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

    def _resolve_did_to_ddo(self, did):
        """resolve a DID to a given DDO, return the DDO if found"""
        did_resolver = DIDResolver(self._ocean._web3, self._ocean._keeper.did_registry)
        resolved = did_resolver.resolve(did)
        if resolved and resolved.is_ddo:
            ddo = DDO(json_text=resolved.value)
            return ddo
        return None

    def _get_endpoint(self, service_type):
        """return the endpoint based on the service service_type"""
        if self._ddo:
            service = self._ddo.get_service(service_type)
            if service:
                endpoints = service.endpoints
                return endpoints[0]
        return None
