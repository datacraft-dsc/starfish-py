"""
    test_10_asset_upload

    As a developer working with Ocean,
    I need a way to create a valid service agreement that I can offer to others for puchase

"""

import secrets

from starfish.asset import MemoryAsset


def test_10_asset_upload(surfer_agent, metadata):
    test_data = secrets.token_hex(1024)
    asset = MemoryAsset(metadata=metadata, data=test_data)
    listing = surfer_agent.register_asset(asset)
    assert(listing)
    assert(listing.asset)

    assert(surfer_agent.upload_asset(listing.asset))
