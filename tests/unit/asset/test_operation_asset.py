"""
    test_operation_asset

"""

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


def test_operation_asset_mode(metadata, config):

    asset = OperationAsset.create('new operation', OPERATION_METADATA)
    for mode_name in OPERATION_METADATA['operation']['modes']:
        assert(asset.is_mode(mode_name))
        assert(not asset.is_mode(f'{mode_name}-badmode'))

