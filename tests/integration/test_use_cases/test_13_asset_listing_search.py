"""
    test_13_asset_listing_search

    As a developer building client code to interact with an Ocean marketplace,
    I need a way to search available asset listings

"""

import secrets

from starfish.asset import DataAsset


def test_13_asset_listing_search(resources, remote_agent_surfer):
    test_data = secrets.token_hex(1024)
    asset_data = DataAsset.create('TestAsset', test_data)
    asset = remote_agent_surfer.register_asset(asset_data)
    assert(asset)
    listing = remote_agent_surfer.create_listing(resources.listing_data, asset.did)
    assert(listing)
    assert(listing.asset_did)
