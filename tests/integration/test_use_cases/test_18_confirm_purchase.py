"""
    test_18_confirm_purchase

    As a developer building a service provider Agent for Ocean,
    I need a way to confirm if an Asset has been sucessfully puchased so that
    I can determine whether to serve the asset to a given requestor

"""

import secrets
import logging
import json

from starfish.asset import DataAsset


def test_18_confirm_purchase(resources, config, remote_agent_surfer, convex_accounts):
    purchaser_account = convex_accounts
    test_data = secrets.token_bytes(1024)
    asset_data = DataAsset.create('TestAsset', test_data)
    asset = remote_agent_surfer.register_asset(asset_data)
    assert(asset)
    listing = remote_agent_surfer.create_listing(resources.listing_data, asset.did)
    listing.set_published(True)
    logging.debug("confirm_purchase for listingid: " + listing.listing_id)
    response = remote_agent_surfer.update_listing(listing)
    logging.debug("update_listing response: " + str(response))
    assert(response)
    status = 'ordered'
    purchase = remote_agent_surfer.purchase_asset(listing, purchaser_account, None, status)
    assert(purchase['listingid'] == listing.listing_id)
    assert(purchase['status'] == status)
