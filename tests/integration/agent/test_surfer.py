"""
    Test Surfer ddo resolver class

"""

import pathlib
import json
import logging
import time
from web3 import Web3
import requests
import pytest

from starfish import Ocean
from starfish.agent import SurferAgent
from starfish.asset import MemoryAsset, Asset
from tests.integration.mocks.surfer_mock import SurferMock
import tests.integration.utils.ddo as ddo
from starfish.models.surfer_model import SurferModel


def test_get_ddo(ocean, metadata, config):

    did,ddoval=ddo.get_ddo(config)
    print(ddoval)
    assert did is not None
    assert ddo is not None

    surfer=SurferAgent(ocean,did=did,ddo=ddoval,options={'authorization':config.authorization})
    assert surfer is not None

    asset=Asset(SurferAgent.generate_metadata())
    listing = surfer.register_asset(asset)
    assert listing is not None
    assert 64==len(listing.listing_id)
    print(listing)
