"""
    test_12_listing_publish

    As a developer working with an Ocean marketplace,
    I need a way to unpublish my asset (i.e. remove relevant listings) from a marketplace

"""

import secrets

from starfish.asset import DataAsset


def test_12_listing_publish(resources, remote_agent):
    test_data = secrets.token_hex(1024)
    asset = DataAsset.create('TestAsset', test_data)
    listing = remote_agent.register_asset(asset, resources.listing_data)
    assert(listing)
    assert(listing.asset)

    assert(not listing.is_published)

    listing.set_published(True)
    assert(listing.is_published)

    assert(remote_agent.update_listing(listing))

    read_listing = remote_agent.get_listing(listing.listing_id)
    assert(read_listing)
    assert(read_listing.is_published)
