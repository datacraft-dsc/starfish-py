"""
    test_07_metadata_access

    As a developer working with Ocean,
    I need a way to request metadata for an arbitrary asset

"""

import secrets
import json

from starfish.asset import DataAsset
from starfish.agent import RemoteAgent
from starfish.ddo.starfish_ddo import StarfishDDO



def test_07_metadata_access(ocean, resources, remote_agent):
    test_data = secrets.token_hex(1024)
    asset_data = DataAsset.create('TestAsset', test_data)
    asset = remote_agent.register_asset(asset_data)
    assert(asset.asset_id)
    assert(asset.metadata)
    assert(asset.metadata == asset_data.metadata)
