"""
    test_12_listing_publish

    As a developer working with an Ocean marketplace,
    I need a way to unpublish my asset (i.e. remove relevant listings) from a marketplace

"""

import secrets

from starfish.asset import DataAsset


def test_12_listing_publish(resources, remote_agent_surfer):
    test_data = secrets.token_hex(1024)
    asset_data = DataAsset.create('TestAsset', test_data)
    asset = remote_agent_surfer.register_asset(asset_data)
    assert(asset)
    listing = remote_agent_surfer.create_listing(resources.listing_data, asset.did)
    assert(listing)
    assert(listing.asset_did)

    assert(not listing.is_published)

    listing.set_published(True)
    assert(listing.is_published)

    assert(remote_agent_surfer.update_listing(listing))

    read_listing = remote_agent_surfer.get_listing(listing.listing_id)
    assert(read_listing)
    assert(read_listing.is_published)
