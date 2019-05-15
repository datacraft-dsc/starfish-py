"""
    test_16_asset_bundle

    As a developer working with asset bundles
    I want a way to get to sub-assets.
    
"""

import secrets
import logging
import json

from starfish.asset import MemoryAsset
from starfish.asset import BundleAsset

TEST_ASSET_COUNT = 4


def test_16_asset_bundle_register(ocean, config, surfer_agent, metadata):
    bundle = BundleAsset()
    asset_list = {}
    for index in range(0, TEST_ASSET_COUNT):
        test_data = secrets.token_hex(1024)
        asset_list[index] = MemoryAsset(metadata=metadata, data=test_data)
        assert(index == bundle.add(asset_list[index]))

    for index, asset in bundle:
        assert(index >=0 and index < TEST_ASSET_COUNT)
        assert(asset.data == asset_list[index].data)
        
        
