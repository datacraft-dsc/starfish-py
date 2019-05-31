"""
    test_squid_asset

"""

import secrets
import logging
import json

from starfish.asset import SquidAsset


def test_init(metadata):
    asset = SquidAsset(metadata)
    assert(asset)
    assert(isinstance(asset, SquidAsset))

