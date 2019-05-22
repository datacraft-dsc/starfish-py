"""
    test_20_invoke_service_free

    As a developer working with Ocean,
    I wish to invoke a free service available on the Ocean ecosystem and obtain the results as a new Ocean Asset

"""

import secrets
import logging
import json

from starfish.asset import MemoryAsset

PRIME_NUMBER_INVOKE_ASSET_ID = "8d658b5b09ade5526aecf669e4291c07d88e9791420c09c51d2f922f721858d1"

def test_19_asset_download(surfer_agent):
    
    # this should be get_listing..
    # listing = surfer_agent.get_listing(listing_id)
    
    # at the moment Koi does not create a listing with the asset, so
    # we need to call get_asset instead
    invoke_asset = surfer_agent.get_asset(PRIME_NUMBER_INVOKE_ASSET_ID)
    assert(invoke_asset)
