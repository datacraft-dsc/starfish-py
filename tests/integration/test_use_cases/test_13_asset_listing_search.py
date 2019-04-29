"""
    test_13_asset_listing_search

    As a developer building client code to interact with an Ocean marketplace,
    I need a way to search available asset listings

"""

import secrets

from starfish.asset import MemoryAsset


def test_13_asset_listing_search(surfer_agent, metadata):
    test_data = secrets.token_hex(1024)
    asset = MemoryAsset(metadata=metadata, data=test_data)
    listing = surfer_agent.register_asset(asset)
    assert(listing)
    assert(listing.asset)
