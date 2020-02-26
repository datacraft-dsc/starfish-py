"""
    test_13_asset_listing_search

    As a developer building client code to interact with an Ocean marketplace,
    I need a way to search available asset listings

"""

import secrets

from starfish.asset import DataAsset


def test_13_asset_listing_search(resources, remote_agent):
    test_data = secrets.token_hex(1024)
    asset_data = DataAsset.create('TestAsset', test_data)
    asset = remote_agent.register_asset(asset_data)
    assert(asset)
    listing = remote_agent.create_listing(resources.listing_data, asset.did)
    assert(listing)
    assert(listing.asset_did)
