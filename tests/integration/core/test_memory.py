"""
    Test ocean class

"""

import datetime
import pathlib
import json
import logging
import time
import secrets
from web3 import Web3

from starfish import Ocean
from starfish.agent import MemoryAgent
from starfish.asset import DataAsset


def _register_asset_for_sale(agent, resources, account):

    asset = DataAsset.create('TestAsset', secrets.token_hex(256))
    listing = agent.register_asset(asset, resources.listing_data, account=account)
    assert listing
    assert listing.asset.did
    return listing

def test_asset(ocean, resources, config, publisher_account, purchaser_account):

    # create an ocean object

    agent = MemoryAgent(ocean)
    assert agent


    listing = _register_asset_for_sale(agent, resources, publisher_account)
    assert listing
    assert publisher_account

    listing_id = listing.listing_id
    # start to test getting the asset from storage
    listing = agent.get_listing(listing_id)
    assert listing
    assert listing.listing_id == listing_id


    # test purchase an asset
    purchase_asset = listing.purchase(purchaser_account)
    assert purchase_asset


    assert(purchase_asset.is_purchased)
    assert(purchase_asset.wait_for_completion())
    assert(purchase_asset.is_completed)
    assert(purchase_asset.is_purchase_valid)

    assert(purchase_asset.consume_asset)



def test_search_listing(ocean, resources, config, publisher_account):

    agent = MemoryAgent(ocean)

    listing = _register_asset_for_sale(agent, resources, publisher_account)
    assert listing
    assert publisher_account

    # choose a word from the description field
    text = resources.listing_data['author']
    words = text.split(' ')
    word = words[0]

    # should return at least 1 or more assets
    logging.info(f'search word is {word}')
    searchResult = agent.search_listings(word)
    assert searchResult

    assert(len(searchResult) > 0)
