import pytest
import pathlib
import json
import datetime
import logging
from unittest.mock import Mock

RESOURCES_PATH = pathlib.Path.cwd() / 'tests' / 'resources'
METADATA_SAMPLE_FILE = RESOURCES_PATH / 'metadata' / 'sample_metadata1.json'
TEST_ASSET_FILE = RESOURCES_PATH / 'test_asset_file.txt'
TEST_ASSET_REMOTE = 'https://oceanprotocol.com/tech-whitepaper.pdf'


# set debug logging
logging.basicConfig(level=logging.DEBUG)


TEST_LISTING_DATA = {
    'name': 'Test file asset',
    'description': 'Test asset for sale',
    'dateCreated': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
    'author': 'Test starfish',
    'license': 'Closed',
    'price': 3.141592,              # price is in ocean tokens
    'extra_data': 'Some extra data',
    'tags': ['asset', 'sale', 'test', 'starfish'],
}


@pytest.fixture(scope="module")
def metadata():
    # load in the sample metadata
    assert METADATA_SAMPLE_FILE.exists(), "{} does not exist!".format(METADATA_SAMPLE_FILE)
    metadata = None
    with open(METADATA_SAMPLE_FILE, 'r') as file_handle:
        metadata = json.load(file_handle)

    return metadata

@pytest.fixture(scope="module")
def resources():
    data = Mock()
    data.asset_file = TEST_ASSET_FILE
    data.metadata = METADATA_SAMPLE_FILE
    data.asset_remote = TEST_ASSET_REMOTE
    data.listing_data = TEST_LISTING_DATA
    return data


