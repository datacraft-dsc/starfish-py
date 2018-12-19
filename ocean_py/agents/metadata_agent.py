"""
    MetadataAgent - Agent to read/write and list metadata on the Ocean network
"""
import json
import re
import requests

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
        if kwargs.get('auth', None):
            self._headers['Authorization'] = 'Basic {}'.format(kwargs.get('auth'))

    def register(self, url, account, did=None):
        return super(MetadataAgent, self).register( METADATA_AGENT_ENDPOINT_NAME, url, account, did)

    def register_asset(self, metadata, **kwargs):
        result = None
        metadata_text = json.dumps(metadata)
        asset_id = MetadataAgent._get_asset_id_from_metadata(metadata_text)
        if self._save(asset_id, metadata_text):
            result = {
                'asset_id': asset_id,
                'did': '{0}/{1}'.format(agent.did, asset_id),
                'metadata_text': metadata_text,
            }
        return result


    def _saveMetadat(self, asset_id, metadata_text):
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

    def _readMetadata(self, asset_id):
        """read the metadata from a service agent using the asset_id"""
        endpoint = self._get_endpoint(METADATA_AGENT_ENDPOINT_NAME)
        if endpoint:
            url = endpoint + METADATA_BASE_URI + '/' + asset_id
            logger.debug('metadata read url {}'.format(url))
            response = requests.get(url, headers=self._headers)
            if response.status_code == requests.codes.ok:
                return response.content.decode('utf-8')
            else:
                logger.warning('metadata asset read {0} response returned {1}'. format(asset_id, response))
        return None

    @staticmethod
    def _get_asset_id_from_metadata(metadata_text):
        """
        return the asset_id calculated from the metadata
        :param metadata: dict of metadata to hash
        a 64 char hex string, which is the asset id
        :return 64 char hex string, with no leading '0x'
        """
        return Web3.toHex(Web3.sha3(metadata_text.encode()))[2:]
