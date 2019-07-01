"""
    test_10_asset_upload

    As a developer working with an Ocean marketplace,
    I need a way to upload my asset with a service agreement

"""

import secrets

from starfish.asset import MemoryAsset


def test_10_asset_upload(resources, surfer_agent):
    test_data = secrets.token_hex(1024)
    asset = MemoryAsset(data=test_data)
    listing = surfer_agent.register_asset(asset, resources.listing_data)
    assert(listing)
    assert(listing.asset)

    assert(surfer_agent.upload_asset(listing.asset))
