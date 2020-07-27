"""
    test_asset_base

"""

import secrets
import logging
import json
import pytest

from starfish.asset import AssetBase
from starfish.utils.did import (
    did_to_id,
    id_to_did,
    decode_to_asset_id,
    did_generate_random
)

ASSET_METADATA = {
    'name': 'Asset',
    'type': 'asset',
}

TEST_DID = did_generate_random()

def test_init(metadata):
    asset = AssetBase(json.dumps(ASSET_METADATA))
    assert(asset)
    assert(isinstance(asset, AssetBase))

def test_metadata():
    asset = AssetBase(json.dumps(ASSET_METADATA))
    assert(asset)
    assert(asset.metadata == ASSET_METADATA)

def test_data():
    asset = AssetBase(json.dumps(ASSET_METADATA))
    assert(asset)
    assert(asset.metadata == ASSET_METADATA)
    asset.set_did(TEST_DID)
    assert(asset.did == TEST_DID)


def test_is_asset_type():
    asset = AssetBase(json.dumps(ASSET_METADATA))
    assert(asset)
    assert(asset.is_asset_type('asset'))
    assert(not asset.is_asset_type('bad asset type'))

def test_asset_id():
    asset = AssetBase(json.dumps(ASSET_METADATA))
    assert(asset)
    asset.set_did(TEST_DID)
    with pytest.raises(ValueError):
        asset_id = decode_to_asset_id(asset.did)

    test_did = did_generate_random()
    asset_id = secrets.token_hex(32)
    asset_did = f'{test_did}/{asset_id}'

    asset = AssetBase(json.dumps(ASSET_METADATA))
    assert(asset)
    asset.set_did(asset.did)
    #assert(asset.asset_id == asset_id)
