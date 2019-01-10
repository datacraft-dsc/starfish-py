"""
    MetadataAgent - Agent to read/write and list metadata on the Ocean network
"""
import json
import re
import requests
from web3 import Web3


from ocean_py.agents.agent import Agent
from ocean_py import logger



# service endpoint type name to use for this agent
METADATA_AGENT_ENDPOINT_NAME = 'metadata-storage'
METADATA_BASE_URI = '/api/v1/meta/data'

class MetadataAgent(Agent):
    def __init__(self, ocean, **kwargs):
        """init a standard ocean agent, with a given DID"""
        Agent.__init__(self, ocean, **kwargs)

        self._headers = {'content-type': 'application/json'}
        if 'authorization' in kwargs and kwargs['authorization']:
            self._headers['Authorization'] = 'Basic {}'.format(kwargs['authorization'])

    def register(self, url, account, did=None):
        return super(MetadataAgent, self).register( METADATA_AGENT_ENDPOINT_NAME, url, account, did)

    def register_asset(self, metadata, **kwargs):
        result = None
        metadata_text = json.dumps(metadata)
        asset_id = self._get_asset_id_from_metadata(metadata_text)
        if self.save(asset_id, metadata_text):
            result = {
                'asset_id': asset_id,
                'did': '{0}/{1}'.format(self._did, asset_id),
                'metadata_text': metadata_text,
            }
        return result


    def save(self, asset_id, metadata_text):
        """save metadata to the agent server, using the asset_id and metadata"""
        endpoint = self._get_endpoint(METADATA_AGENT_ENDPOINT_NAME)
        if endpoint:
            url = endpoint + METADATA_BASE_URI + '/' + asset_id
            logger.debug('metadata save url {}'.format(url))
            response = requests.put(url, data=metadata_text, headers=self._headers)
            if response.status_code == requests.codes.ok:
                return asset_id
            else:
                logger.warning('metadata asset read {0} response returned {1}'. format(asset_id, response))
        return None

    def read_asset(self, asset_id):
        """read the metadata from a service agent using the asset_id"""
        result = None
        endpoint = self._get_endpoint(METADATA_AGENT_ENDPOINT_NAME)
        if endpoint:
            url = endpoint + METADATA_BASE_URI + '/' + asset_id
            logger.debug('metadata read url {}'.format(url))
            response = requests.get(url, headers=self._headers)
            if response.status_code == requests.codes.ok:
                result = {
                    'asset_id': asset_id,
                    'did': '{0}/{1}'.format(self._did, asset_id),
                    'metadata_text': response.content.decode('utf-8')
                }
            else:
                logger.warning('metadata asset read {0} response returned {1}'. format(asset_id, response))
        return result


    def is_metadata_valid(self, asset_id, metadata_text):
        """
        validate metadata, by calcualating the hash (asset_id) and compare this to the
        given asset_id, if both are equal then the metadata is valid
        :param asset_id: asset id to compare with
        :param metadata: dict of metadata to calculate the hash ( asset_id)
        :return bool True if metadata is valid for the asset_id provided
        """
        if metadata_text:
            # the calc asset_id from the metadata should be same as this asset_id
            metadata_id = self._get_asset_id_from_metadata(metadata_text)
            if metadata_id != asset_id:
                logger.debug('metdata has does not match {0} != {1}'.format(metadata_id, asset_id))
            return metadata_id == asset_id
        return False
        

    def _get_asset_id_from_metadata(self, metadata_text):
        """
        return the asset_id calculated from the metadata
        :param metadata: dict of metadata to hash
        a 64 char hex string, which is the asset id
        :return 64 char hex string, with no leading '0x'
        """
        return Web3.toHex(Web3.sha3(metadata_text.encode()))[2:]
