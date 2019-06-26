"""
    test_pd_case_file_transfer

    As a developer
    I want save an asset file on surfer, and sale the asset via squid,
    As a consumer
    I want to purchase an asset vi Ocean and download the asset from Sufer.

"""

import secrets
import logging
import json

from starfish.asset import (
    FileAsset,
    RemoteAsset,
)
from tests.integration.libs.helpers import setup_squid_purchase

def test_pd_case_file_transfer(ocean, config, resources, surfer_agent, squid_agent):
    
    # take copy of the stored data to compare later
    with open(resources.asset_file, 'rb') as fp:
        store_data = fp.read()
        
    # save the asset file to surfer
    asset_store = FileAsset(filename=resources.asset_file)
    listing_store = surfer_agent.register_asset(asset_store, resources.listing_data)
    assert(listing_store)
    
    # now upload to the storage
    surfer_agent.upload_asset(asset_store)
    
    # now register the asset link to surfer in squid
    publisher_account = ocean.get_account(config.publisher_account)
    download_link = asset_store.did
    asset_sale = RemoteAsset(url=download_link)
    listing = squid_agent.register_asset(asset_sale, resources.listing_data, account=publisher_account)
    assert(listing)


    # now start the purchase part
    # setup the purchase account
    purchase_account = ocean.get_account(config.purchaser_account)
    logging.info(f'purchase_account {purchase_account.ocean_balance}')
    purchase_account.unlock()
    # request the tokens to buy the asset
    purchase_account.request_tokens(10)

    setup_squid_purchase(ocean, listing, publisher_account)

    # purchase the linked remote asset
    purchase = listing.purchase(purchase_account)
    assert(purchase)

    assert(not purchase.is_completed)

    error_message = purchase.wait_for_completion()
    assert(error_message == True)

    assert(purchase.is_completed)


    assert(purchase.is_purchased)
    assert(purchase.is_purchase_valid)

    purchase_asset = purchase.consume
    assert(purchase_asset)
        
    print(purchase_asset.url)
    assert(purchase_asset.url)
    surfer_did, asset_id = surfer_agent.decode_asset_did(purchase_asset.url)
    download_url = surfer_agent.get_asset_store_url(asset_id)
    
    store_asset = surfer_agent.download_asset(asset_id, download_url)
    assert(store_asset)
    assert(store_asset.is_asset_type('data'))
    assert(store_asset.data == store_data)
