import pytest
import os
import logging
import json
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
           path_items = url_split.path.split('/')
           assert(len(path_items) > 4)
           assert(path_items[1] == 'api')
           assert(path_items[2] == 'v1')
           assert(path_items[3] == 'meta')

           if path_items[4] == 'data':
               return self.put_data(path_items[5], data)
        return SurferMock._response(401, 'Error')

    def put_data(self, asset_id, metadata):
       Asset_storage[asset_id] = metadata
       new_asset_id = Web3.toHex(Web3.sha3(metadata.encode()))[2:]
       return SurferMock._response(200, new_asset_id)


    @staticmethod
    def _response(status=200, content="CONTENT", json_data=None):
        response = Mock()
        response.status_code = status
        response.content = content
        # add json data
        if json_data:
            response.json = Mock(return_value=json_data)
        return response
