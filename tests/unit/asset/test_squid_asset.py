"""
    test_squid_asset

"""

import secrets
import logging
import json

from starfish.asset import RemoteAsset


def test_init(metadata):
    asset = RemoteAsset(metadata)
    assert(asset)
    assert(isinstance(asset, RemoteAsset))

