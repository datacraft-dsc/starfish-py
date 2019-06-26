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
    
    # save the asset file to surfer
    asset_store = FileAsset(filename=resources.asset_file)
    listing_store = surfer_agent.register_asset(asset_store, resources.listing_data)
    assert(listing_store)
    
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
    purchase_asset = listing.purchase(purchase_account)
    assert purchase_asset

    assert(not purchase_asset.is_completed(purchase_account))

    error_message = purchase_asset.wait_for_completion(purchase_account)
    assert(error_message == True)

    assert(purchase_asset.is_completed(purchase_account))


    assert(purchase_asset.is_purchased)
    assert(purchase_asset.is_purchase_valid(purchase_account))


    model = ocean.get_squid_model()
    squid_ocean = model.get_squid_ocean(purchase_account)
    ddo = squid_ocean.assets.resolve(listing.asset.did)
    files_str = squid_ocean.secret_store.decrypt(
            ddo.asset_id, 
            ddo.encrypted_files, 
            purchase_account._squid_account
    )
    print(files_str)
    
    
    logging.debug("asset_download for listingid: " + listing_store.listing_id + " = asset_id: " +  asset_store.asset_id)
    asset2 = surfer_agent.download_asset(asset_store.asset_id)
    logging.debug("download_asset response: " + str(asset2))
    # assert(asset2)
