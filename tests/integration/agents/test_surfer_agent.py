"""
    Test Surfer Agent class

"""

import pathlib
import json
import logging
import time
from web3 import Web3

from starfish import Ocean
from starfish.agent import SurferAgent
from starfish.asset import MemoryAsset
from tests.integration.helpers.surfer_mock import SurferMock
from starfish.models.surfer_model import SurferModel

from starfish.logging import setup_logging

CONFIG_PARAMS = {'contracts_path': 'artifacts', 'keeper_url': 'http://localhost:8545' }

METADATA_SAMPLE_PATH = pathlib.Path.cwd() / 'tests' / 'resources' / 'metadata' / 'sample_metadata1.json'
REGISTER_ACCOUNT = { 'address': '0x00bd138abd70e2f00903268f3db08f2d25677c9e', 'password': 'node0'}

SURFER_URL = 'http://localhost:8080'

def _read_metadata():
    # load in the sample metadata
    assert METADATA_SAMPLE_PATH.exists(), "{} does not exist!".format(METADATA_SAMPLE_PATH)
    metadata = None
    with open(METADATA_SAMPLE_PATH, 'r') as file_handle:
        metadata = json.load(file_handle)

    return metadata

def _create_memory_asset():
    metadata = _read_metadata()
    assert metadata
    return MemoryAsset(metadata['base'])

def _register_asset_for_sale(agent, account):
    asset = _create_asset()
    listing = agent.register_asset(asset, account=account)
    assert listing
    assert listing.asset.did
    return listing

def _log_event(event_name):
    def _process_event(event):
        logging.debug(f'Received event {event_name}: {event}')
    return _process_event

def test_asset():

    # create an ocean object
    ocean = Ocean(CONFIG_PARAMS, log_level=logging.DEBUG)

    assert ocean
    assert ocean.accounts

    # we first need to register the Surfer agent with a did/ddo on chain
    register_account = ocean.get_account(REGISTER_ACCOUNT)

    agent_did, ddo, private_key_pem = ocean.register_update_agent_service(SurferAgent.endPointName, SURFER_URL, register_account)

    surferMock = SurferMock(SURFER_URL)
    SurferModel.set_http_client(surferMock)


    agent = SurferAgent(ocean, agent_did, ddo)
    assert agent

    asset = _create_memory_asset()
    assert(asset)

    print(asset.did)
    listing = agent.register_asset(asset)
    assert(listing)
    asset_did = listing.asset.did

    listing = agent.get_listing(asset_did)
    print(listing)
