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


def test_18_confirm_purchase(ocean, resources, config, remote_agent, purchaser_account):
    test_data = secrets.token_hex(1024)
    asset = DataAsset.create('TestAsset', test_data)
    listing = remote_agent.register_asset(asset, resources.listing_data)
    listing.set_published(True)
    logging.debug("confirm_purchase for listingid: " + listing.listing_id)
    response = remote_agent.update_listing(listing)
    logging.debug("update_listing response: " + str(response))
    assert(response)
    status = 'ordered'
    purchase = remote_agent.purchase_asset(listing, purchaser_account, None, status)
    assert(purchase['listingid'] == listing.listing_id)
    assert(purchase['status'] == status)
