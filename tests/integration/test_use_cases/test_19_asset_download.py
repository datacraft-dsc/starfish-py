"""
    test_19_asset_download

    As a developer working with an Ocean marketplace,
    I want to record a purchase.

"""

import secrets
import logging
import json

from starfish.asset import MemoryAsset


def test_19_asset_download(surfer_agent, metadata):
    test_data = secrets.token_hex(1024)
    asset = MemoryAsset(metadata=metadata, data=test_data)
    listing = surfer_agent.register_asset(asset)
    logging.debug("asset_download for listingid: " + listing.listing_id + " = asset_id: " +  asset.asset_id)
    asset2 = surfer_agent.download_asset(asset.asset_id)
    logging.debug("download_asset response: " + str(asset2))
    # FIXME SurferAgent.download_asset under development
    # assert(asset2.asset_id == asset.asset_id)
    # assert(asset2.data == asset.data)
