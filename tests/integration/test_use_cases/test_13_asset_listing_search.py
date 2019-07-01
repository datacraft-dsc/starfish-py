"""
    test_13_asset_listing_search

    As a developer building client code to interact with an Ocean marketplace,
    I need a way to search available asset listings

"""

import secrets

from starfish.asset import MemoryAsset


def test_13_asset_listing_search(resources, surfer_agent):
    test_data = secrets.token_hex(1024)
    asset = MemoryAsset(data=test_data)
    listing = surfer_agent.register_asset(asset, resources.listing_data)
    assert(listing)
    assert(listing.asset)
