import pytest
import pathlib
import json
from unittest.mock import Mock

RESOURCES_PATH = pathlib.Path.cwd() / 'tests' / 'resources'
METADATA_SAMPLE_FILE = RESOURCES_PATH / 'metadata' / 'sample_metadata1.json'
TEST_ASSET_FILE = RESOURCES_PATH / 'test_asset_file.txt'
TEST_ASSET_REMOTE = 'https://oceanprotocol.com/tech-whitepaper.pdf'


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
    return data
