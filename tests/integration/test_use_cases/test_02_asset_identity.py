"""
    test_02_asset_identity
    
"""

import secrets
from starfish.asset import MemoryAsset
from starfish.agent import SurferAgent


def test_02_asset_register(ocean, surfer_agent):
    asset = MemoryAsset(data=secrets.token_hex(1024))
    listing = surfer_agent.register_asset(asset)
    assert(not listing is None)
    assert(64==len(listing.listing_id))
    assert(listing.asset.data == asset.data)


def test_02_asset_upload(ocean, surfer_agent):
    asset = MemoryAsset(data=secrets.token_hex(1024))
    listing = surfer_agent.register_asset(asset)
    surfer_agent.upload_asset(listing.asset)
