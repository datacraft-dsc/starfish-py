"""
    test_08_asset_registration

    As a developer working with Ocean,
    I need a way to register a new asset with Ocean

"""

import secrets
import json

from starfish.asset import DataAsset
from starfish.agent import RemoteAgent


def test_08_asset_registration(resources, remote_agent):
    test_data = secrets.token_hex(1024)
    description = secrets.token_hex(16)
    asset_data_1 = DataAsset.create('TestAsset_08', test_data, {'description': description})
    asset_1 = remote_agent.register_asset(asset_data_1)
    assert(asset_1)

    asset_data_2 = DataAsset.create('TestAsset_08', test_data,  {'description': description})
    asset_2 = remote_agent.register_asset(asset_data_2)
    assert(asset_2)

    assert(asset_1.asset_id == asset_2.asset_id)

    asset_list = remote_agent.search_asset({
        'name': 'TestAsset_08',
         'description': description,
    })
    assert(asset_list)
    assert(len(asset_list) > 0)
    assert(asset_list[0] == asset_1.asset_id)
