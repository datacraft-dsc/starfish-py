"""
    test_07_metadata_access

    As a developer working with Ocean,
    I need a way to request metadata for an arbitrary asset

"""

import secrets
import json

from starfish.asset import MemoryAsset
from starfish.agent import SurferAgent
from starfish.ddo.starfish_ddo import StarfishDDO



def test_07_metadata_access(ocean, resources, surfer_agent):
    test_data = secrets.token_hex(1024)
    asset = MemoryAsset(data=test_data)
    listing = surfer_agent.register_asset(asset, resources.listing_data)
    assert(not listing is None)
    assert(listing.listing_id)
    store_listing = surfer_agent.get_listing(listing.listing_id)
    assert(store_listing)
    assert(store_listing.asset.asset_id)
    assert(store_listing.asset.metadata)
    assert(store_listing.asset.metadata == listing.asset.metadata)
