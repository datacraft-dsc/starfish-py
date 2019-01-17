"""
    Test ocean class

"""

import pathlib
import json
import logging

from ocean_py.ocean import Ocean
from ocean_py.logging import setup_logging
from ocean_py import logger

from squid_py.service_agreement.service_factory import ServiceDescriptor
from squid_py.utils.utilities import generate_new_id
from squid_py import ACCESS_SERVICE_TEMPLATE_ID


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

def test_asset():
    # create an ocean object
    ocean = Ocean(CONFIG_PARMS)
    assert ocean
    assert ocean.accounts

    # test node has the account #1 unlocked
    publisher_account = ocean.accounts[list(ocean.accounts)[1]]

    # load in the sample metadata
    assert METADATA_SAMPLE_PATH.exists(), "{} does not exist!".format(METADATA_SAMPLE_PATH)
    metadata = None
    with open(METADATA_SAMPLE_PATH, 'r') as file_handle:
        metadata = json.load(file_handle)
    assert metadata

    # as of squid-0.1.22 - price is set in the metadata
    #service_descriptors = [ServiceDescriptor.access_service_descriptor(asset_price)]

    asset = ocean.register_asset(metadata, account=publisher_account)
    assert asset
    assert asset.did
    
    asset_did = asset.did
    # start to test getting the asset from storage
    asset = ocean.get_asset(asset_did)
    assert asset
    assert asset.did == asset_did
    purchase_account = ocean.accounts[list(ocean.accounts)[1]]
    purchase_account.request_tokens(100)
    
    # test purchase an asset
    asset.purchase(purchase_account)
     
    
