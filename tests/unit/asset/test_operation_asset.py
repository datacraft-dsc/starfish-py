"""
    test_operation_asset

"""

import pytest
import secrets
import logging
import json

from starfish.asset import OperationAsset

OPERATION_METADATA = {
    'name': 'operation',
    'type': 'operation',
    'operation': {
        'modes': ['sync', 'async', 'test'],
    },
}


def test_init(metadata):
    asset = OperationAsset.create('new operation', OPERATION_METADATA)
    assert(asset)
    assert(isinstance(asset, OperationAsset))
    assert(asset.type_name == 'operation')


def test_operation_asset_create():
    asset_name = secrets.token_hex(8)

    asset = OperationAsset.create(asset_name)
    assert(asset)
    assert(asset.name == asset_name)

    values = {
        'name': 'value',
        'key1': secrets.randbelow(100000)
    }
    test_data = json.dumps(values)

    asset = OperationAsset.create(asset_name, metadata = {}, data = test_data)
    assert(asset)
    assert(asset.name == asset_name)
    assert(asset.type_name == 'operation')
    assert(asset.data == json.dumps(values).encode())
    assert(not asset.is_orchestration)


def test_operation_create_orchestration():
    asset_name = secrets.token_hex(8)

    values = {
        'name': 'value',
        'key1': secrets.randbelow(100000)
    }
    asset = OperationAsset.create_orchestration(asset_name, values)
    assert(asset)
    assert(asset.name == asset_name)
    assert(asset.type_name == 'operation')
    assert(asset.data == json.dumps(values).encode())
    assert(asset.is_orchestration)

    with pytest.raises(TypeError, match='ochestration data can only'):
        asset = OperationAsset.create_orchestration(asset_name, ['invalid', 'list'])


def test_operation_asset_mode(metadata, config):

    asset = OperationAsset.create('new operation', OPERATION_METADATA)
    for mode_name in OPERATION_METADATA['operation']['modes']:
        assert(asset.is_mode(mode_name))
        assert(not asset.is_mode(f'{mode_name}-badmode'))



