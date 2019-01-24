"""
    MetadataAgent - Agent to read/write and list metadata on the Ocean network
"""
import json
import requests
from web3 import Web3

from squid_py.did_resolver.did_resolver import DIDResolver
from squid_py.ddo import DDO

from ocean_py.agent.agent_base import AgentBase
from ocean_py import logger

# service endpoint type name to use for this agent
METADATA_MARKET_AGENT_ENDPOINT_NAME = 'metadata-storage'
METADATA_MARKET_BASE_URI = '/api/v1/meta/data'

class MetadataMarketAgent(AgentBase):
    def __init__(self, ocean):
        """init a standard ocean agent, with a given DID"""
        AgentBase.__init__(self, ocean)

        self._did = kwargs.get('did')
        self._ddo = None
        self._register_name = METADATA_MARKET_AGENT_ENDPOINT_NAME

        # if DID then try to load in the linked DDO
        if self._did:
            self._ddo = self._resolve_did_to_ddo(self._did)

        self._headers = {'content-type': 'application/json'}
        if 'authorization' in kwargs and kwargs['authorization']:
            self._headers['Authorization'] = f'Basic {kwargs["authorization"]}'

    def register_asset(self, metadata):
        """
        Register an asset with the agent storage server
        :param metadata: metadata to write to the storage server

        """
        result = None
        metadata_text = json.dumps(metadata)
        asset_id = MetadataMarketAgent.get_asset_id_from_metadata(metadata_text)
        if self.save(asset_id, metadata_text):
            result = {
                'asset_id': asset_id,
                'did': f'{self._did}/{asset_id}',
                'metadata_text': metadata_text,
            }
        return result

    def save(self, asset_id, metadata_text):
        """save metadata to the agent server, using the asset_id and metadata"""
        endpoint = self._get_endpoint(METADATA_MARKET_AGENT_ENDPOINT_NAME)
        if endpoint:
            url = endpoint + METADATA_MARKET_BASE_URI + '/' + asset_id
            logger.debug(f'metadata save url {url}')
            response = requests.put(url, data=metadata_text, headers=self._headers)
            if response and response.status_code == requests.codes.ok:
                return asset_id
            logger.warning(f'metadata asset read {asset_id} response returned {response}')
        return None

    def read_asset(self, asset_id):
        """read the metadata from a service agent using the asset_id"""
        result = None
        endpoint = self._get_endpoint(METADATA_MARKET_AGENT_ENDPOINT_NAME)
        if endpoint:
            url = endpoint + METADATA_MARKET_BASE_URI + '/' + asset_id
            logger.debug(f'metadata read url {url}')
            response = requests.get(url, headers=self._headers)
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
            metadata_id = MetadataMarketAgent.get_asset_id_from_metadata(metadata_text)
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

    def _resolve_did_to_ddo(self, did):
        """resolve a DID to a given DDO, return the DDO if found"""
        did_resolver = DIDResolver(self._ocean.web3, self._ocean.keeper.did_registry)
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
                return service.get_endpoint()
        return None
