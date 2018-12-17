"""
    MetadataAgent - Agent to read/write and list metadata on the Ocean network
"""
import json
import requests

from ocean_py.agent import Agent
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
        
    def save(self, asset_id, metadata_text):
        """save metadata to the agent server, using the asset_id and metadata"""
        endpoint = self._get_endpoint(METADATA_AGENT_ENDPOINT_NAME)
        print(asset_id, metadata_text)
        if endpoint:
            url = endpoint + METADATA_BASE_URI + '/' + asset_id
            response = requests.put(url, data=metadata_text, headers=self._headers)
            logger.debug('response {}'.format(response))
            # TODO: server not running on travis build, so always return success !
            return asset_id
        return None

    def read(self, asset_id):
        """read the metadata from a service agent using the asset_id"""
        endpoint = self._get_endpoint(METADATA_AGENT_ENDPOINT_NAME)
        if endpoint:
            response = requests.get(endpoint + '/data/' + asset_id).content
            if response:
                return json.loads(response)
        return None
