"""
    Test ocean class

"""

import pathlib
import json
import logging

from ocean_py.ocean import Ocean
from ocean_py.agents.metadata_agent import MetadataAgent
from ocean_py.agents.squid_agent import SquidAgent

from ocean_py.logging import setup_logging
from ocean_py import logger

from squid_py.service_agreement.service_factory import ServiceDescriptor
from squid_py.utils.utilities import generate_new_id


setup_logging(level=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("web3").setLevel(logging.WARNING)

CONFIG_PARMS = {
    'contracts_path': 'artifacts',
    'keeper_url': 'http://localhost:8545',
    'secret_store_url': 'http://localhost:12001',
    'parity_url': 'http://localhost:8545',
    'parity_address': '0x00bd138abd70e2f00903268f3db08f2d25677c9e',
    'parity_password': 'node0',
}


METADATA_SAMPLE_PATH = pathlib.Path.cwd() / 'tests' / 'resources' / 'metadata' / 'sample_metadata1.json'

def test_asset_on_chain():
    # create an ocean object
    ocean = Ocean(CONFIG_PARMS)
    assert ocean
    assert ocean.keeper
    assert ocean.web3
    assert ocean.accounts

    # test node has the account #1 unlocked
    publisher_account = ocean.accounts[list(ocean.accounts)[1]]

    # load in the sample metadata
    assert METADATA_SAMPLE_PATH.exists(), "{} does not exist!".format(METADATA_SAMPLE_PATH)
    metadata = None
    with open(METADATA_SAMPLE_PATH, 'r') as file_handle:
        metadata = json.load(file_handle)
    assert metadata

    # test registering an asset
    asset_price = 100
    #service_descriptors = [ServiceDescriptor.access_service_descriptor(asset_price)]

    asset = ocean.register_asset(metadata, account=publisher_account, price=asset_price)
    assert asset

    asset_did = asset.did
    # start to test getting the asset from storage
    asset = ocean.get_asset(asset_did)
    assert asset
