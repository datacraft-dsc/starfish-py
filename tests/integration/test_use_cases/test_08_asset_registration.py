"""
    test_08_asset_registration

    As a developer working with Ocean,
    I need a way to register a new asset with Ocean

"""

import secrets
import json

from starfish.asset import DataAsset
from starfish.agent import RemoteAgent
from starfish.ddo.starfish_ddo import StarfishDDO



def test_08_asset_registration(resources, remote_agent):
    test_data = secrets.token_hex(1024)
    asset1 = DataAsset.create('TestAsset', test_data)
    listing1 = remote_agent.register_asset(asset1, resources.listing_data)
    assert(listing1)
    assert(listing1.asset)

    asset2 = DataAsset.create('TestAsset', test_data)
    listing2 = remote_agent.register_asset(asset2, resources.listing_data)
    assert(listing2)
    assert(listing2.asset)

    assert(listing1.asset.asset_id == listing2.asset.asset_id)
