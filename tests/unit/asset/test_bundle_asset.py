"""
    test_bundle_asset

"""

import secrets
import logging
import json

from starfish.asset import DataAsset
from starfish.asset import BundleAsset

TEST_ASSET_COUNT = 4


def test_init():
    bundle = BundleAsset.create('Bundle Asset')
    assert(bundle)

    bundle = BundleAsset({
        'name': 'Bundle Asset',
        'type': 'bundle'
    })
    assert(bundle)

def test_bundle_asset_add_access_remove(config):
    bundle = BundleAsset.create('name')
    asset_list = {}

    assert(bundle.is_bundle)
    # add a set of memory assets

    for index in range(0, TEST_ASSET_COUNT):
        test_data = secrets.token_hex(1024)
        name = f'name_{index}'
        asset_list[name] = DataAsset.create(f'Asset_{index}', test_data)
        bundle.add(name, asset_list[name])
        assert(bundle[name])
        assert(bundle.asset_count == index + 1)

    # using the iterator
    for name, asset in bundle:
        assert(name)
        assert(asset)
        assert(asset.data == asset_list[name].data)

    # using the get_asset and __getitem__
    for index in range(0, bundle.asset_count):
        asset = bundle.get_asset(index)
        name = list(asset_list.keys())[index]
        assert(asset.data == asset_list[name].data)
        asset = bundle.get_asset(name)
        assert(asset)
        assert(asset.data == asset_list[name].data)
        asset = bundle[name]
        assert(asset)
        assert(asset.data == asset_list[name].data)

        items = dict(bundle.asset_items)
        asset = items[name]
        assert(asset)
        assert(asset.data == asset_list[name].data)



    # test remove
    for name in bundle.asset_names:
        asset = bundle.asset_remove(name)
        assert(asset)

    assert(bundle.asset_count == 0)
