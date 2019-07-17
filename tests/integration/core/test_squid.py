"""
    Test ocean class

"""

import datetime
import pathlib
import json
import logging
import time
import secrets
import pytest

from web3 import Web3

from starfish import Ocean
from starfish.models.squid_model import SquidModel
from starfish.agent import SquidAgent
from starfish.asset import (
    FileAsset,
    RemoteAsset,
)
from starfish.exceptions import (
    StarfishAssetNotFound,
    StarfishPurchaseError
)

from squid_py.agreements.service_factory import ServiceDescriptor
from squid_py.utils.utilities import generate_new_id

from squid_py.brizo.brizo_provider import BrizoProvider
from squid_py.aquarius.aquarius import Aquarius
from squid_py.ddo.ddo import DDO

logger = logging.getLogger('test.core.test_squid')

def _register_asset_for_sale(agent, resources, account):

    asset = FileAsset(filename=resources.asset_file)
    listing = agent.register_asset(asset, resources.listing_data, account=account)
    assert(listing)
    assert(listing.asset.did)
    return(listing)


def test_asset_file_register(ocean, config, resources):
    publisher_account = ocean.get_account(config.publisher_account)

    agent = SquidAgent(ocean, config.squid_config)
    assert(agent)

    asset = FileAsset(filename=resources.asset_file)
    listing = agent.register_asset(asset, resources.listing_data, publisher_account)
    assert(listing)


def test_asset_remote_register(ocean, config, resources):
    publisher_account = ocean.get_account(config.publisher_account)

    agent = SquidAgent(ocean, config.squid_config)
    assert(agent)

    asset = RemoteAsset(url=resources.asset_remote)

    listing = agent.register_asset(asset, resources.listing_data, publisher_account)
    assert(listing)


def is_purchase_allowed(did, agreement_id, publish_account, conusmer_account):

    logger.debug(f'is purchase allowed {did}, {agreement_id}, {publish_account}, {conusmer_account}')
    return True

def test_asset(ocean, config, resources):

    agent = SquidAgent(ocean, config.squid_config)
    assert(agent)


    # test node has the account #0 unlocked
    publisher_account = ocean.get_account(config.publisher_account)
    publisher_account.unlock()
    publisher_account.request_tokens(20)

    listing = _register_asset_for_sale(agent, resources, publisher_account)
    assert(listing)
    assert(publisher_account)

    listing_did = listing.asset.did
    # start to test getting the asset from storage
    listing = agent.get_listing(listing_did)
    assert(listing)
    assert(listing.asset.did == listing_did)



    purchase_account = ocean.get_account(config.purchaser_account)
    logger.info(f'purchase_account {purchase_account.ocean_balance}')

    # test is_purchased for an account only
    assert(not listing.is_purchased(purchase_account))

    purchase_account.unlock()

    purchase_account.request_tokens(10)


    time.sleep(1)
    logger.info(f'purchase_account after token request {purchase_account.ocean_balance}')


    agent.start_agreement_events_monitor(publisher_account, is_purchase_allowed)

    # test purchase an asset
    purchase_asset = listing.purchase(purchase_account)
    assert(purchase_asset)

    assert(not purchase_asset.is_completed)

    error_message = purchase_asset.wait_for_completion()
    assert(error_message == True)

    assert(purchase_asset.is_completed)

    # assert Web3.toHex(event.args['_agreementId']) == agreement_id
    # assert len(os.listdir(consumer_ocean_instance.config.downloads_path)) == downloads_path_elements + 1

    # This test does not work with the current barge

    assert(purchase_asset.is_purchased)
    assert(purchase_asset.is_purchase_valid)


    # test getting a list of purchase ids from a listing
    purchase_ids = listing.get_purchase_ids
    assert(purchase_ids)
    assert(len(purchase_ids) == 1)
    assert(purchase_ids[0] == purchase_asset.purchase_id)

    # test is_purchased for an account only
    assert(listing.is_purchased(purchase_account))

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
    logger.info(f'search word is {word}')
    search_result = agent.search_listings(word)
    assert(search_result)

    assert(len(search_result) > 1)

def test_get_listing(ocean, config, resources):
    agent = SquidAgent(ocean, config.squid_config)
    # test node has the account #0 unlocked
    publisher_account = ocean.get_account(config.publisher_account)
    publisher_account.unlock()

    listing = _register_asset_for_sale(agent, resources, publisher_account)
    assert listing
    assert publisher_account

    found_listing = agent.get_listing(listing.listing_id)
    assert(found_listing)

    # now test for an asset in aquarius but not on the block chain network

    aquarius = Aquarius(config.squid_config['aquarius_url'])
    ddo = aquarius.get_asset_ddo(listing.listing_id)
    dummy_listing_id = f'did:op:{generate_new_id()}'
    ddo_dict = ddo.as_dictionary()
    ddo_dict['id'] = dummy_listing_id
    # fix squid index bug in service list ?
    index = 0
    for service in ddo_dict['service']:
        ddo_dict['service'][index]['serviceDefinitionId'] = index

    dummy_ddo = DDO(dictionary=ddo_dict)
    aquarius.publish_asset_ddo(dummy_ddo)

    ddo = aquarius.get_asset_ddo(dummy_listing_id)
    assert(ddo.did == dummy_listing_id)

    # the final test, the asset did is in aquarius, but the did -> url is not on the block chain
    with pytest.raises(StarfishAssetNotFound):
        dummy_listing = agent.get_listing(dummy_listing_id)

    # now try to purchase an invalid asset with no block chain DID
    purchase_account = ocean.get_account(config.purchaser_account)

    listing_list = agent.search_listings({'tags': ['starfish']})
    assert(listing_list)
    for listing in listing_list:
        assert(listing)
        if listing.listing_id == dummy_listing_id:
            with pytest.raises(StarfishAssetNotFound):
                listing.purchase(purchase_account)

def test_insufficient_funds(ocean, config, resources):
    publisher_account = ocean.get_account(config.publisher_account)

    agent = SquidAgent(ocean, config.squid_config)
    assert(agent)

    asset = FileAsset(filename=resources.asset_file)
    listing_data = resources.listing_data.copy()
    listing_data['price'] = 83454.2345
    listing = agent.register_asset(asset, listing_data, publisher_account)
    assert(listing)

    listing_did = listing.asset.did
    # start to test getting the asset from storage
    listing = agent.get_listing(listing_did)

    purchase_account = ocean.get_account(config.purchaser_account)
    with pytest.raises(StarfishPurchaseError):
        purchase_asset = listing.purchase(purchase_account)
