"""
    Test ocean class

"""

import datetime
import pathlib
import json
import logging
import time
from web3 import Web3

from starfish import Ocean
from starfish.models.squid_model import SquidModel
from starfish.agent import SquidAgent
from starfish.asset import (
    FileAsset,
    RemoteAsset,
)

from starfish.logging import setup_logging
from tests.integration.libs.helpers import setup_squid_purchase

from squid_py.agreements.service_factory import ServiceDescriptor
from squid_py.utils.utilities import generate_new_id

from squid_py.brizo.brizo_provider import BrizoProvider

def _register_asset_for_sale(agent, resources, account):

    asset = FileAsset(filename=resources.asset_file)
    listing = agent.register_asset(asset, resources.listing_data, account=account)
    assert listing
    assert listing.asset.did
    return listing


def test_asset_file_register(ocean, config, resources):
    publisher_account = ocean.get_account(config.publisher_account)

    agent = SquidAgent(ocean, config.squid_config)
    assert agent

    asset = FileAsset(filename=resources.asset_file)
    listing = agent.register_asset(asset, resources.listing_data, publisher_account)
    assert(listing)


def test_asset_remote_register(ocean, config, resources):
    publisher_account = ocean.get_account(config.publisher_account)

    agent = SquidAgent(ocean, config.squid_config)
    assert agent

    asset = RemoteAsset(url=resources.asset_remote)

    listing = agent.register_asset(asset, resources.listing_data, publisher_account)
    assert(listing)
    print(listing.ddo.as_text())


def test_asset(ocean, config, resources):

    agent = SquidAgent(ocean, config.squid_config)
    assert agent


    # test node has the account #0 unlocked
    publisher_account = ocean.get_account(config.publisher_account)
    publisher_account.unlock()
    publisher_account.request_tokens(20)

    listing = _register_asset_for_sale(agent, resources, publisher_account)
    assert listing
    assert publisher_account

    listing_did = listing.asset.did
    # start to test getting the asset from storage
    listing = agent.get_listing(listing_did)
    assert listing
    assert listing.asset.did == listing_did

    purchase_account = ocean.get_account(config.purchaser_account)
    logging.info(f'purchase_account {purchase_account.ocean_balance}')

    purchase_account.unlock()

    purchase_account.request_tokens(10)

    time.sleep(1)
    logging.info(f'purchase_account after token request {purchase_account.ocean_balance}')

    setup_squid_purchase(ocean, listing, publisher_account)

    # test purchase an asset
    purchase_asset = listing.purchase(purchase_account)
    assert purchase_asset

    assert(not purchase_asset.is_completed)

    error_message = purchase_asset.wait_for_completion()
    assert(error_message == True)

    assert(purchase_asset.is_completed)

    # assert Web3.toHex(event.args['_agreementId']) == agreement_id
    # assert len(os.listdir(consumer_ocean_instance.config.downloads_path)) == downloads_path_elements + 1

    # This test does not work with the current barge

    assert purchase_asset.is_purchased
    assert purchase_asset.is_purchase_valid

    remote_asset = purchase_asset.consume_asset
    assert(remote_asset)



def test_search_listing(ocean, config, resources):


    agent = SquidAgent(ocean, config.squid_config)

    # test node has the account #0 unlocked
    publisher_account = ocean.get_account(config.publisher_account)
    publisher_account.unlock()

    listing = _register_asset_for_sale(agent, resources, publisher_account)
    assert listing
    assert publisher_account

    # choose a word from the description field
    text = resources.listing_data['author']
    words = text.split(' ')
    word = words[0]

    # should return at least 1 or more assets
    logging.info(f'search word is {word}')
    search_result = agent.search_listings(word)
    assert(search_result)

    assert(len(search_result) > 1)
