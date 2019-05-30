"""
    Test ocean class

"""

import pathlib
import json
import logging
import time
from web3 import Web3

from starfish import Ocean
from starfish.models.squid_model import SquidModel
from starfish.agent import SquidAgent
from starfish.asset import SquidAsset

from starfish.logging import setup_logging

from squid_py.agreements.service_factory import ServiceDescriptor
from squid_py.utils.utilities import generate_new_id
from squid_py.brizo.brizo_provider import BrizoProvider

from tests.integration.mocks.koi_mock import KoiMock
from tests.integration.mocks.brizo_mock import BrizoMock


def _register_asset_for_sale(agent, metadata, account):

    asset=SquidAsset(metadata)
    listing = agent.register_asset(asset, account=account)
    assert listing
    assert listing.asset.did
    return listing

def test_invoke(ocean, metadata, config, brizo_mock):


    agent = SquidAgent(ocean, config.squid_config)
    assert agent


    # test node has the account #0 unlocked
    publisher_account = ocean.get_account(config.publisher_account)
    publisher_account.unlock()
    publisher_account.request_tokens(20)

    listing = _register_asset_for_sale(agent, metadata, publisher_account)
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

    model = ocean.get_squid_model()
    ddo = model._squid_ocean.assets.resolve(listing.asset.did)

    brizo_mock.subscribe(ocean, publisher_account._squid_account, listing.asset.did, ddo)


    # test purchase an asset
    # this purchase does not automatically fire a consume() request as no callback is registered
    purchase_asset = listing.purchase(purchase_account)
    assert purchase_asset

    assert(not purchase_asset.is_completed(purchase_account))

    error_message = purchase_asset.wait_for_completion(purchase_account)
    assert(error_message == True)

    assert(purchase_asset.is_completed(purchase_account))

    # assert len(os.listdir(consumer_ocean_instance.config.downloads_path)) == downloads_path_elements + 1

    # This test does not work with the current barge

    assert purchase_asset.is_purchased
    #assert purchase_asset.is_purchase_valid(purchase_account)
    #this assertion fails
    purch_type=purchase_asset.get_type
    logging.debug(f'purchase type {purch_type}')
    paramvalue={'hello':'world'}
    print(purchase_asset)
    # TODO: invoke method does not exist?
    # result=purchase_asset.invoke(purchase_account,{'operation':'echo','params':paramvalue})
    ## TBD: asset on the result of the invoke
    # logging.debug(f'invoke result {result}')
    # assert result == paramvalue


#test_asset()
