"""
    test_10_asset_upload

    As a developer working with an Ocean marketplace,
    I need a way to upload my asset with a service agreement

"""

import secrets

from starfish.asset import DataAsset


def test_10_asset_upload(resources, remote_agent_surfer):
    test_data = secrets.token_hex(1024)
    asset_data = DataAsset.create('TestAsset', test_data)
    asset = remote_agent_surfer.register_asset(asset_data)
    assert(asset)

    assert(remote_agent_surfer.upload_asset(asset))
