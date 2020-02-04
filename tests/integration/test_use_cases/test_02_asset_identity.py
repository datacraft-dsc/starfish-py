"""
    test_02_asset_identity


    As a developer working with Ocean,
    I need a stable identifier (Asset ID) for an arbitrary asset in the Ocean ecosystem

"""

import secrets
from starfish.asset import DataAsset
from starfish.agent import RemoteAgent

# TEST_TEXT = "Django raspberrypi diversity goat python. Cython raspberrypi community dict import object coroutine arduino. Python raspberrypi beautiful pypy gevent pycon raspberrypi rocksdahouse method. Return integration mercurial pypi dunder. Reduce integration itertools test import. Future raspberrypi exception list."

def test_02_asset_register(ocean, resources, remote_agent):
    testData = secrets.token_hex(1024)
    asset1 = DataAsset.create('TestAsset1', testData)
    asset2 = DataAsset.create('TestAsset2', testData)
    listing = remote_agent.register_asset(asset2, resources.listing_data)
    assert(not listing is None)
    assert(64==len(listing.listing_id))
    assert(listing.asset.data == asset2.data)
    assert(listing.asset.asset_id == asset2.asset_id)


def test_02_asset_upload(ocean, resources, remote_agent):
    testData = secrets.token_hex(1024)
    asset = DataAsset.create('TestAsset', testData)
    listing = remote_agent.register_asset(asset, resources.listing_data)
    remote_agent.upload_asset(listing.asset)
