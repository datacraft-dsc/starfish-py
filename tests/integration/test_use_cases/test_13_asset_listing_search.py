"""
    test_13_asset_listing_search

    As a developer building client code to interact with an Ocean marketplace,
    I need a way to search available asset listings

"""

import secrets

from starfish.asset import DataAsset


def test_13_asset_listing_search(resources, remote_agent):
    test_data = secrets.token_hex(1024)
    asset = DataAsset.create('TestAsset', test_data)
    listing = remote_agent.register_asset(asset, resources.listing_data)
    assert(listing)
    assert(listing.asset)
