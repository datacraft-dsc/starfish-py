"""
    test_19_asset_download

    As a developer working with an Ocean marketplace,
    I want to record a purchase.

"""

import secrets
import logging
import json

from starfish.asset import MemoryAsset


def test_19_asset_download(resources, surfer_agent):
    test_data = secrets.token_hex(1024)
    asset = MemoryAsset(data=test_data)
    listing = surfer_agent.register_asset(asset, resources.listing_data)
    
    url = surfer_agent.get_asset_store_url(asset.asset_id)
    surfer_agent.upload_asset(asset)
    
    # now download
    store_asset = surfer_agent.download_asset(asset.asset_id, url)
    
    assert(store_asset)
    assert(store_asset.data == asset.data.encode())
    assert(store_asset.asset_id == asset.asset_id)
