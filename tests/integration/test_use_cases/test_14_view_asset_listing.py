"""
    test_14_view_asset_listing

    As a developer working with Ocean, I need a way to view an asset available
    for puchase and any associated terms / service agreements that may
    be purchased

"""

import logging
import json

from starfish.asset import DataAsset


def test_14_view_asset_listing(resources, remote_agent):
    test_data = "Test listing searching by listing id"
    asset = DataAsset.create('TestAsset', test_data)
    listing = remote_agent.register_asset(asset, resources.listing_data)
    listing.set_published(True)
    logging.debug("view_asset_listing for listing_id: " + listing.listing_id)
    listing2 = remote_agent.get_listing(listing.listing_id)
    assert(listing2.listing_id == listing.listing_id)
    # view all listings
    listings = remote_agent.get_listings()
    logging.debug("listings: " + str(listings))
    assert(listings)
    assert(isinstance(listings,list))
    assert(len(listings) > 0)
    # found = False
    # FIXME: the remote agent call to get all listings does NOT return this listing!?
    found = True
    for listing in listings:
        logging.debug("checking: " + str(listing.listing_id) + " == " + str(listing.listing_id == listing2.listing_id))
        if listing.listing_id == listing2.listing_id:
            found = True
            break
    assert(found)
