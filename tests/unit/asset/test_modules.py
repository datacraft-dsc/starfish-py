"""

Test asset modules in __init__.py

"""
import secrets
import logging
import json

from starfish.asset import (
    create_asset_from_metadata,
    AssetBase,
    MemoryAsset,
    SquidAsset,
    BundleAsset,
    OperationAsset,
    Asset,
)


def test_create_asset_from_metadata(metadata):
    asset = create_asset_from_metadata(metadata)
    assert(asset)
    assert(isinstance(asset, SquidAsset))

    type_list = [
        ( 'bundle', BundleAsset ), 
        ( 'data', MemoryAsset ),
        ( 'memory', MemoryAsset ),
        ( 'operation', OperationAsset ),
        ( 'unknown', Asset ),
    ]
    for type_name, class_type in type_list:
        metadata = {
            'type': type_name
        }
        asset = create_asset_from_metadata(metadata)
        assert(asset)
        assert(isinstance(asset, class_type))
