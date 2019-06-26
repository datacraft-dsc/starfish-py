"""
    test_02_asset_identity


    As a developer working with Ocean,
    I need a stable identifier (Asset ID) for an arbitrary asset in the Ocean ecosystem

"""

import secrets
from starfish.asset import MemoryAsset
from starfish.agent import SurferAgent


def test_02_asset_register(ocean, resources, surfer_agent):
    test_data = secrets.token_hex(1024)
    asset1 = MemoryAsset(data=test_data)
    asset2 = MemoryAsset(data=test_data)
    listing = surfer_agent.register_asset(asset2, resources.listing_data)
    assert(not listing is None)
    assert(64==len(listing.listing_id))
    assert(listing.asset.data == asset2.data)
    assert(listing.asset.asset_id == asset2.asset_id)


def test_02_asset_upload(ocean, resources, surfer_agent):
    asset = MemoryAsset(data=secrets.token_hex(1024))
    listing = surfer_agent.register_asset(asset, resources.listing_data)
    surfer_agent.upload_asset(listing.asset)
