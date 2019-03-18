"""


This class mocks the Surfer web service api.

I have been trying to get as close as the current surfer API, including the error
messages returned

see https://github.com/DEX-Company/surfer/blob/develop/src/main/clojure/surfer/handler.clj

"""

import pytest
import os
import logging
import json
import re

from urllib.parse import urlparse
from web3 import Web3

from unittest.mock import Mock

from starfish.logging import setup_logging

setup_logging(level=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("web3").setLevel(logging.WARNING)

Asset_storage = {}


class SurferMock(object):

    def __init__(self, url):
        self._url = url


    def put(self, url, data=None, headers=None):
        url_split = urlparse(url)
        assert(url_split)
        if url_split.path:
            if not re.match('^/api/v1/meta', url_split.path):
                return SurferMock._repsonse(404, 'path not found')
            path_items = url_split.path.split('/')
            if len(path_items) < 4:
                return SurferMock._repsonse(404, 'path not found')

            if path_items[4] == 'data' and len(path_items) > 5:
               return self.put_metadata(path_items[5], data)
        return SurferMock._response(400, 'Bad request')


    def put_metadata(self, asset_id, metadata):
        Asset_storage[asset_id] = metadata
        asset_hash = Web3.toHex(Web3.sha3(metadata.encode()))[2:]
        if asset_hash == asset_id:
            return SurferMock._response(200, asset_hash)
        return SurferMock._response(400, f'Invalid ID for metadata, expcted: "{asset_hash}" got "{asset_id}"')


    @staticmethod
    def _response(status=200, content="CONTENT", json_data=None):
        response = Mock()
        response.status_code = status
        response.content = content
        # add json data
        if json_data:
            response.json = Mock(return_value=json_data)
        return response
