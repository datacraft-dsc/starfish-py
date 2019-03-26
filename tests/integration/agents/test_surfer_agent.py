"""
    Test Surfer Agent class

"""

import pathlib
import json
import logging
import time
from web3 import Web3

from starfish import Ocean
from starfish.agent import SurferAgent
from starfish.asset import MemoryAsset
from tests.integration.mocks.surfer_mock import SurferMock
from starfish.models.surfer_model import SurferModel



def _log_event(event_name):
    def _process_event(event):
        logging.debug(f'Received event {event_name}: {event}')
    return _process_event

def test_asset(ocean, metadata, config):

    # we first need to register the Surfer agent with a did/ddo on chain
    register_account = ocean.get_account(config.publisher_account)

    agent_did, ddo, private_key_pem = ocean.register_update_agent_service(SurferAgent.endPointName, config.surfer_url, register_account)

    surferMock = SurferMock(config.surfer_url)
    SurferModel.set_http_client(surferMock)


    agent = SurferAgent(ocean, agent_did, ddo)
    assert agent

    asset =  MemoryAsset(metadata['base'])
    assert(asset)

    print(asset.did)
    listing = agent.register_asset(asset)
    assert(listing)
    asset_did = listing.asset.did

    listing = agent.get_listing(asset_did)
    print(listing)
