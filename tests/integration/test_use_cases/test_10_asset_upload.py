"""
    test_10_asset_upload

    As a developer working with an Ocean marketplace,
    I need a way to upload my asset with a service agreement

"""

import secrets

from starfish.asset import DataAsset


def test_10_asset_upload(resources, remote_agent):
    test_data = secrets.token_hex(1024)
    asset = DataAsset.create('TestAsset', test_data)
    listing = remote_agent.register_asset(asset, resources.listing_data)
    assert(listing)
    assert(listing.asset)

    assert(remote_agent.upload_asset(listing.asset))
