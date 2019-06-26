"""
    test_08_asset_registration

    As a developer working with Ocean,
    I need a way to register a new asset with Ocean

"""

import secrets
import json

from starfish.asset import MemoryAsset
from starfish.agent import SurferAgent
from starfish.ddo.starfish_ddo import StarfishDDO



def test_08_asset_registration(resources, surfer_agent):
    test_data = secrets.token_hex(1024)
    asset1 = MemoryAsset(data=test_data)
    listing1 = surfer_agent.register_asset(asset1, resources.listing_data)
    assert(listing1)
    assert(listing1.asset)

    asset2 = MemoryAsset(data=test_data)
    listing2 = surfer_agent.register_asset(asset2, resources.listing_data)
    assert(listing2)
    assert(listing2.asset)

    assert(listing1.asset.asset_id == listing2.asset.asset_id)
