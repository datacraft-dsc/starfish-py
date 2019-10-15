"""

Test asset modules in __init__.py

"""
import secrets
import logging
import json

from starfish.asset import (
    create_asset_from_metadata_text,
    AssetBase,
    BundleAsset,
    DataAsset,
    OperationAsset,
)


def test_create_asset_from_metadata():

    type_list = [
        ( 'bundle', BundleAsset ),
        ( 'dataset', DataAsset ),
        ( 'operation', OperationAsset ),
    ]
    for type_name, class_type in type_list:
        metadata = {
            'type': type_name,
            'name': f'TestAsset_{type_name}'
        }
        asset = create_asset_from_metadata_text(json.dumps(metadata))
        assert(asset)
        assert(isinstance(asset, class_type))
