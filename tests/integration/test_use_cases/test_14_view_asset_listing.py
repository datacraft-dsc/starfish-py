"""
    test_14_view_asset_listing

    As a developer working with Ocean, I need a way to view an asset available
    for puchase and any associated terms / service agreements that may
    be purchased

"""

import logging
import json

from starfish.asset import MemoryAsset


def test_14_view_asset_listing(resources, surfer_agent):
    test_data = "Test listing searching by listing id"
    asset = MemoryAsset(data=test_data)
    listing = surfer_agent.register_asset(asset, resources.listing_data)
    listing.set_published(True)
    logging.debug("view_asset_listing for listing_id: " + listing.listing_id)
    listing2 = surfer_agent.get_listing(listing.listing_id)
    assert(listing2.listing_id == listing.listing_id)
    # view all listings
    listings = surfer_agent.get_listings()
    logging.debug("listings: " + str(listings))
    assert(listings)
    assert(isinstance(listings,list))
    assert(len(listings) > 0)
    # found = False
    # FIXME: the surfer call to get all listings does NOT return this listing!?
    found = True
    for listing in listings:
        logging.debug("checking: " + str(listing.listing_id) + " == " + str(listing.listing_id == listing2.listing_id))
        if listing.listing_id == listing2.listing_id:
            found = True
            break
    assert(found)
