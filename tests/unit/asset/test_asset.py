"""
    test_asset

"""

import secrets
import logging
import json

from starfish.asset import Asset

ASSET_METADATA = {
    'name': 'Asset',
    'type': 'asset',
}


def test_init(metadata):
    asset = Asset(ASSET_METADATA)
    assert(asset)
    assert(isinstance(asset, Asset))


