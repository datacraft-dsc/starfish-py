"""
    test_asset_base

"""

import secrets
import logging
import json
import pytest

from starfish.asset import (
    AssetBase,
    create_asset_provenance_publish,
    create_asset_provenance_invoke
)

from starfish.network.did import (
    did_to_id,
    id_to_did,
    decode_to_asset_id,
    did_generate_random
)

ASSET_METADATA = {
    'name': 'Asset',
    'type': 'dataset',
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
    asset = AssetBase(json.dumps(ASSET_METADATA), did=TEST_DID)
    assert(asset)
    assert(asset.metadata == ASSET_METADATA)
    assert(asset.did == TEST_DID)


def test_is_asset_type():
    asset = AssetBase(json.dumps(ASSET_METADATA))
    assert(asset)
    assert(asset.is_asset_type('dataset'))
    assert(not asset.is_asset_type('bad asset type'))

def test_asset_id():
    asset = AssetBase(json.dumps(ASSET_METADATA), did=TEST_DID)
    assert(asset)
    with pytest.raises(ValueError):
        asset_id = decode_to_asset_id(asset.did)

    test_did = did_generate_random()
    asset_id = secrets.token_hex(32)
    asset_did = f'{test_did}/{asset_id}'

    asset = AssetBase(json.dumps(ASSET_METADATA), did=asset_did)
    assert(asset)
    #assert(asset.asset_id == asset_id)

def test_asset_create_asset_provenance_publish():
    agent_did = did_generate_random()
    asset = AssetBase(json.dumps(ASSET_METADATA))
    assert(asset)
    asset = create_asset_provenance_publish(asset, agent_did)
    assert(asset.metadata['provenance'])


def test_asset_create_asset_provenance_invoke():
    agent_did = did_generate_random()
    job_id = secrets.token_hex(32)
    inputs_text = json.dumps(
        {
            'asset_list': 'json'
        }
    )
    asset = AssetBase(json.dumps(ASSET_METADATA))
    assert(asset)
    asset = create_asset_provenance_invoke(asset, agent_did, job_id, None, inputs_text)
    assert(asset.metadata['provenance'])
