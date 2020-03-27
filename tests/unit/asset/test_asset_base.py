"""
    test_asset_base

"""

import secrets
import logging
import json

from starfish.asset import AssetBase
from starfish.utils.did import (
    did_to_id,
    id_to_did,
    decode_to_asset_id
)

ASSET_METADATA = {
    'name': 'Asset',
    'type': 'asset',
}

TEST_DID = id_to_did(secrets.token_hex(32))

def test_init(metadata):
    asset = AssetBase(ASSET_METADATA)
    assert(asset)
    assert(isinstance(asset, AssetBase))

def test_metadata():
    asset = AssetBase(ASSET_METADATA)
    assert(asset)
    assert(asset.metadata == ASSET_METADATA)

def test_data():
    asset = AssetBase(ASSET_METADATA, TEST_DID)
    assert(asset)
    assert(asset.metadata == ASSET_METADATA)
    assert(asset.did == TEST_DID)


def test_is_asset_type():
    asset = AssetBase(ASSET_METADATA)
    assert(asset)
    assert(asset.is_asset_type('asset'))
    assert(not asset.is_asset_type('bad asset type'))

def test_asset_id():
    asset = AssetBase(ASSET_METADATA, TEST_DID)
    assert(asset)
    asset_id = decode_to_asset_id(asset.did)
    print(asset_id, asset.asset_id)

    assert(asset.asset_id == asset_id)

    did_id = secrets.token_hex(32)
    path_did = id_to_did(did_id)
    asset_id = decode_to_asset_id(f'{path_did}/{asset_id}')

    asset = AssetBase(ASSET_METADATA, f'{path_did}/{asset_id}')
    assert(asset)
    assert(asset.asset_id == asset_id)
