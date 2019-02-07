"""
    Test ocean class

"""

import pathlib
import json
import logging

from starfish_py.ocean import Ocean
from starfish_py.agent.metadata_market_agent import MetadataMarketAgent

from starfish_py.logging import setup_logging
from starfish_py import logger

from squid_py.service_agreement.service_factory import ServiceDescriptor


setup_logging(level=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("web3").setLevel(logging.WARNING)
logging.getLogger("keeper").setLevel(logging.WARNING)

CONTRACTS_PATH = 'artifacts'
KEEPER_URL = 'http://localhost:8545'

METADATA_STORAGE_URL = 'http://localhost:8080'
METADATA_STORAGE_AUTH = 'QWxhZGRpbjpPcGVuU2VzYW1l'
METADATA_SAMPLE_PATH = pathlib.Path.cwd() / 'tests' / 'resources' / 'metadata' / 'sample_metadata1.json'


def test_asset_light():
    
    """
    First part register the agent and get it's DID for later use
    """
    # create an ocean object
    ocean = Ocean( keeper_url=KEEPER_URL, contract_path=CONTRACTS_PATH)
    assert ocean
    assert ocean.keeper
    assert ocean.accounts

    # in testing only account #1 is left unlocked
    agent_account = ocean.accounts[list(ocean.accounts)[1]]

    agent = MetadataMarketAgent(ocean)
    # test register a new metadata storage agent
    did, ddo, private_key_pem = ocean.register_agent(agent, METADATA_STORAGE_URL, agent_account)
    assert private_key_pem
    assert did
    assert ddo

    agent_did = did
    
    """
    Now re-connect to Ocean using the agent's DID and Auth access codes
    """

    # load in the sample metadata
    assert METADATA_SAMPLE_PATH.exists(), "{} does not exist!".format(METADATA_SAMPLE_PATH)
    metadata = None
    with open(METADATA_SAMPLE_PATH, 'r') as file_handle:
        metadata = json.load(file_handle)
    assert metadata


    ocean = Ocean( 
        keeper_url=KEEPER_URL, 
        contract_path=CONTRACTS_PATH, 
    )

    # test registering an asset using an agent object
    asset = ocean.register_asset_light(
        metadata['base'], 
        did=agent_did, 
        authorization=METADATA_STORAGE_AUTH
    )
    assert asset


    asset_did = asset.did
    # start to test getting the asset from storage
    asset = ocean.get_asset(asset_did, authorization=METADATA_STORAGE_AUTH)
    assert asset
