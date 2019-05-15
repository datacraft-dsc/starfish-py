"""
    test_bundle_asset

"""

import secrets
import logging
import json

from starfish.asset import MemoryAsset
from starfish.asset import BundleAsset

TEST_ASSET_COUNT = 4

    
def test_init(metadata):
    bundle = BundleAsset()
    assert(bundle)

    
def test_bundle_asset_iteration(ocean, metadata, config):
    bundle = BundleAsset()
    asset_list = {}
    # add a set of memory assets
    for index in range(0, TEST_ASSET_COUNT):
        test_data = secrets.token_hex(1024)
        asset_list[index] = MemoryAsset(metadata=metadata, data=test_data)
        assert(index == bundle.add(asset_list[index]))

    # using the iterator
    for index, asset in bundle:
        assert(index >=0 and index < TEST_ASSET_COUNT)
        assert(asset.data == asset_list[index].data)
    
    # using the subscriptable __getitem
    for index in range(0, bundle.count):
        asset = bundle[index]
        assert(index >=0 and index < TEST_ASSET_COUNT)
        assert(asset.data == asset_list[index].data)
        
    # test pop
    while bundle.count > 0:
        asset = bundle.pop()
        assert(asset)

    # add back in 
    for index in range(0, TEST_ASSET_COUNT):
        test_data = secrets.token_hex(1024)
        asset_list[index] = MemoryAsset(metadata=metadata, data=test_data)
        assert(index == bundle.add(asset_list[index]))
    
    # test remove
    while bundle.count > 0:
        asset = bundle.remove(0)
        assert(asset)
