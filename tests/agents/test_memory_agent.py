"""
    Test ocean class

"""

import pathlib
import json
import logging
import time
from web3 import Web3

from starfish import (
    Ocean,
    logger
)
from starfish.agent import MemoryAgent

from starfish.logging import setup_logging


setup_logging(level=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("web3").setLevel(logging.WARNING)

CONFIG_PARAMS = {'contracts_path': 'artifacts', 'keeper_url': 'http://localhost:8545' }

PUBLISHER_ACCOUNT = { 'address': '0x00bd138abd70e2f00903268f3db08f2d25677c9e', 'password': 'node0'}
PURCHASER_ACCOUNT = {'address': '0x068Ed00cF0441e4829D9784fCBe7b9e26D4BD8d0', 'password': 'secret'}

METADATA_SAMPLE_PATH = pathlib.Path.cwd() / 'tests' / 'resources' / 'metadata' / 'sample_metadata1.json'

def _read_metadata():
    # load in the sample metadata
    assert METADATA_SAMPLE_PATH.exists(), "{} does not exist!".format(METADATA_SAMPLE_PATH)
    metadata = None
    with open(METADATA_SAMPLE_PATH, 'r') as file_handle:
        metadata = json.load(file_handle)

    return metadata

def _register_asset_for_sale(agent, account):


    metadata = _read_metadata()
    assert metadata

    listing = agent.register_asset(metadata, account=account)
    assert listing
    assert listing.asset.did
    return listing

def _log_event(event_name):
    def _process_event(event):
        logging.debug(f'Received event {event_name}: {event}')
    return _process_event

def test_asset():

    # create an ocean object
    ocean = Ocean(CONFIG_PARAMS)
    assert ocean
    assert ocean.accounts

    agent = MemoryAgent(ocean)
    assert agent


    # test node has the account #0 unlocked
    publisher_account = ocean.get_account(PUBLISHER_ACCOUNT)

    listing = _register_asset_for_sale(agent, publisher_account)
    assert listing
    assert publisher_account

    listing_did = listing.asset.did
    # start to test getting the asset from storage
    listing = agent.get_listing(listing_did)
    assert listing
    assert listing.asset.did == listing_did


    purchase_account = ocean.get_account(PURCHASER_ACCOUNT)

    # test purchase an asset
    purchase_asset = listing.purchase(purchase_account)
    assert purchase_asset

    assert purchase_asset.is_purchased
    assert purchase_asset.is_purchase_valid(purchase_account)

    purchase_asset.consume(purchase_account, '')



def test_search_listing():

    ocean = Ocean(CONFIG_PARAMS)
    assert ocean
    assert ocean.accounts

    agent = MemoryAgent(ocean)

    # test node has the account #0 unlocked
    publisher_account = ocean.get_account(PUBLISHER_ACCOUNT)

    listing = _register_asset_for_sale(agent, publisher_account)
    assert listing
    assert publisher_account

    metadata = _read_metadata()
    assert metadata

    # choose a word from the description field
    text = metadata['base']['description']
    words = text.split(' ')
    word = words[0]

    # should return at least 1 or more assets
    logging.info(f'search word is {word}')
    searchResult = agent.search_listings(word)
    assert searchResult

    assert(len(searchResult) > 0)
