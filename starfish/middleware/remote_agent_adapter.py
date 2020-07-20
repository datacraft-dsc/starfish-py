"""
    RemoteAgentAdapter - Adapter to access the Remote Services
"""
import io
import logging
from urllib.parse import urljoin

import requests

from starfish.utils.crypto_hash import hash_sha3_256

logger = logging.getLogger(__name__)


class ResponseWrapper():
    """
    Response object returned by different test and production
    systems are not the same, and have different properties to obtain
    data and JSON data.

    This class tries to obtain the correct call to get the data from the
    Response object.

    """
    def __init__(self, response):
        self._response = response

    @property
    def json(self):
        if hasattr(self._response, 'get_json'):
            data = self._response.get_json()
        elif hasattr(self._response, 'json'):
            data = self._response.json()
        else:
            TypeError('cannot get the json property from response object')
        return data

    @property
    def data(self):
        if hasattr(self._response, 'content'):
            data = self._response.content
        elif hasattr(self._response, 'data'):
            data = self._response.data
        else:
            raise TypeError('Cannot find correct response data')
        return data


class RemoteAgentAdapter():
    _http_client = requests

    def __init__(self):
        pass

    def register_asset(self, metadata, url, authorization_token=None):
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
        saved_asset_id = self.save_metadata(metadata, url, authorization_token)
        result = {
                'asset_id': saved_asset_id,
                'metadata': metadata,
                'hash': hash_sha3_256(metadata)
            }
        return result

    def get_metadata_list(self, url, authorization_token=None):
        """ return a list of metadata stored on this agent """
        url = urljoin(f'{url}/', 'index')
        logger.debug(f'metadata list url {url}')
        headers = RemoteAgentAdapter.create_headers('application/json', authorization_token)
        response = RemoteAgentAdapter._http_client.get(url, headers=headers)
        if response and response.status_code == requests.codes.ok:
            data = ResponseWrapper(response).json
            return data
        else:
            msg = f'metadata asset response failed: {response.status_code}'
            logger.error(msg)
            raise ValueError(msg)

    def save_metadata(self, metadata, url, authorization_token=None):
        """save metadata to the agent server, using the asset_id and metadata"""
        url = urljoin(f'{url}/', 'data')
        logger.debug(f'metadata save url {url}')
        headers = RemoteAgentAdapter.create_headers('text/plain', authorization_token)
        response = RemoteAgentAdapter._http_client.post(url, data=metadata, headers=headers)
        if response and response.status_code == requests.codes.ok:
            data = ResponseWrapper(response).json
            return data
        else:
            msg = f'metadata asset response failed: {response.status_code}'
            logger.error(msg)
            raise ValueError(msg)
        return None

    def create_listing(self, listing_data, asset_id, url, authorization_token=None):
        data = {
            'assetid': asset_id,
            'info': listing_data,
        }

        url = urljoin(f'{url}/', 'listings')
        headers = RemoteAgentAdapter.create_headers('application/json', authorization_token)
        response = RemoteAgentAdapter._http_client.post(url, json=data, headers=headers)
        if response and response.status_code == requests.codes.ok:
            data = ResponseWrapper(response).json
            logger.debug('listing response returned: ' + str(data))
            return data
        else:
            msg = f'listing response failed: {response.status_code} {response.text}'
            logger.error(msg)
            raise ValueError(msg)
        return None

    def download_asset(self, asset_id, url, authorization_token=None):
        url = urljoin(f'{url}/', asset_id)

        headers = RemoteAgentAdapter.create_headers('application/octet-stream', authorization_token)
        response = RemoteAgentAdapter._http_client.get(url, headers=headers)
        if response and response.status_code == requests.codes.ok:
            data = ResponseWrapper(response).data
            return data
        else:
            msg = f'GET assets response failed: {response.status_code} {response}'
            logger.error(msg)
            raise ValueError(msg)
        return None

    def get_listing(self, listing_id, url, authorization_token=None):
        url = urljoin(f'{url}/', f'listings/{listing_id}')
        headers = RemoteAgentAdapter.create_headers('application/json', authorization_token)
        response = RemoteAgentAdapter._http_client.get(url, headers=headers)
        if response and response.status_code == requests.codes.ok:
            data = ResponseWrapper(response).json
            return data
        else:
            msg = f'GET listings response failed: {response.status_code}'
            logger.error(msg)
            raise ValueError(msg)
        return None

    def get_listings(self, url,  authorization_token=None):
        url = urljoin(f'{url}/', 'listings')
        headers = RemoteAgentAdapter.create_headers('application/json', authorization_token)
        response = RemoteAgentAdapter._http_client.get(url, headers=headers)
        if response and response.status_code == requests.codes.ok:
            return ResponseWrapper(response).json
        else:
            msg = f'GET listings response failed: {response.status_code}'
            logger.error(msg)
            raise ValueError(msg)
        return None

    def update_listing(self, listing_id, data, url, authorization_token=None):
        url = urljoin(f'{url}/', f'listings/{listing_id}')

        headers = RemoteAgentAdapter.create_headers('application/json', authorization_token)
        response = RemoteAgentAdapter._http_client.put(url, json=data, headers=headers)
        if response and response.status_code == requests.codes.ok:
            return True
        else:
            msg = f'PUT listings response failed: {response.status_code}'
            logger.error(msg)
            raise ValueError(msg)
        return None

    def upload_asset_data(self, asset_id, data, url, authorization_token=None):
        url = urljoin(f'{url}/', asset_id)

        logger.debug(f'uploading data to {url}')
        files = {
            'file': (asset_id, io.BytesIO(data), 'application/octet-stream'),
        }
        headers = RemoteAgentAdapter.create_headers(None, authorization_token)
        response = RemoteAgentAdapter._http_client.post(url, files=files, headers=headers)
        if response and (response.status_code == requests.codes.ok or response.status_code == requests.codes.created):
            return True
        else:
            msg = f'upload asset response failed: {response.status_code}:{response.text}'
            logger.error(msg)
            raise ValueError(msg)
        return None

    def read_metadata(self, asset_id, url, authorization_token=None):
        """read the metadata from a service agent using the asset_id"""

        result = None
        url = urljoin(f'{url}/', f'data/{asset_id}')
        logger.debug(f'metadata read url {url}')
        headers = RemoteAgentAdapter.create_headers('text/plain', authorization_token)
        response = RemoteAgentAdapter._http_client.get(url, headers=headers)
        if response and response.status_code == requests.codes.ok:
            data = ResponseWrapper(response).data
            result = {
                'asset_id': asset_id,
                'metadata_text': data,
            }
            result['hash'] = hash_sha3_256(result['metadata_text'])
            # convert to str if bytes
            if isinstance(result['metadata_text'], bytes):
                result['metadata_text'] = data.decode('utf-8')
        else:
            logger.warning(f'metadata asset read {asset_id} response returned {response} for {url}')
        return result

    def purchase_asset(self, purchase, url, authorization_token=None):
        """record purchase"""
        url = urljoin(f'{url}/', 'purchases')
        logger.debug(f'market url for purchases {url}')
        headers = RemoteAgentAdapter.create_headers('application/json', authorization_token)
        response = RemoteAgentAdapter._http_client.post(url, json=purchase, headers=headers)
        if response and response.status_code == requests.codes.ok:
            data = ResponseWrapper(response).json
            logger.debug(f'purchase response returned {data}')
            return data
        else:
            msg = f'purchase response failed: {response.status_code}'
            logger.error(msg)
            # NOTE surfer may return error information in additon to a 500
            if response:
                if hasattr(response, 'get_json'):
                    data = response.get_json()
                elif hasattr(response, 'json'):
                    data = response.json()
                else:
                    TypeError('cannot get the json property from response object')
                logger.error(f'purchase response returned {data}')
            raise ValueError(msg)
        return None

    def invoke(self, asset_id, inputs, url, authorization_token=None):
        """

        call the invoke based on the asset_id without leading 0x
        """

        url = urljoin(f'{url}/', asset_id)
        headers = RemoteAgentAdapter.create_headers('application/json', authorization_token)
        response = RemoteAgentAdapter._http_client.post(url, json=inputs, headers=headers)
        if response and (response.status_code == requests.codes.ok or response.status_code == 201):
            data = ResponseWrapper(response).json
            logger.debug('invoke response returned: ' + str(data))
            return data
        else:
            msg = f'invoke response failed: {response.status_code} {response} for {url}'
            logger.error(msg)
            raise ValueError(msg)
        return None

    def get_job(self, job_id, url, authorization_token=None):
        url = urljoin(f'{url}/', job_id)
        headers = RemoteAgentAdapter.create_headers('application/json', authorization_token)
        response = RemoteAgentAdapter._http_client.get(url, headers=headers)
        if response and response.status_code == requests.codes.ok:
            data = ResponseWrapper(response).json
            return data
        else:
            msg = f'GET job response failed: {response.status_code} for {url}'
            logger.error(msg)
            raise ValueError(msg)
        return None

    def get_authorization_token(self, username, password, url):
        """Get a surfer authorization token (create one if needed).
        Throws exception on error."""
        response = RemoteAgentAdapter._http_client.get(url, auth=(username, password))
        token = None
        if response.status_code == 200:
            tokens = ResponseWrapper(response).json
            if len(tokens) > 0:
                token = tokens[-1]
            else:   # need to create a token
                response = RemoteAgentAdapter._http_client.post(url, auth=(username, password))
                if response.status_code == 200:
                    token = ResponseWrapper(response).json
                else:
                    msg = f'unable to create token, status {response.status_code}'
                    logger.error(msg)
                    raise ValueError(msg)
        else:
            msg = f'unable to get tokens, status {response.status_code}'
            logger.error(msg)
            raise ValueError(msg)
        logger.debug(f'using surfer token {token}')
        return token

    def get_ddo(self, url, authorization_token=None):
        ddo_text = None
        url = urljoin(f'{url}/', '/api/ddo')
        logger.debug(f'get_ddo url {url}')

        headers = RemoteAgentAdapter.create_headers('application/json', authorization_token)
        response = RemoteAgentAdapter._http_client.get(url, headers=headers)
        if response.status_code == 200:
            ddo_text = ResponseWrapper(response).data.decode('utf-8')
        return ddo_text

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
            metadata_id = RemoteAgentAdapter.get_asset_id_from_metadata(metadata_text)
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
        return hash_sha3_256(metadata_text)

    @staticmethod
    def set_http_client(http_client):
        """Set the http client to something other than the default `requests`"""
        RemoteAgentAdapter._http_client = http_client

    @staticmethod
    def create_headers(content_type=None, authorization_token=None):
        headers = {}
        if content_type:
            headers['content-type'] = content_type
        if authorization_token:
            headers['Authorization'] = f'token {authorization_token}'
        if headers == {}:
            return None
        return headers
