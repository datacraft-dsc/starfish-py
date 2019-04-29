
import pytest
import secrets
import tempfile


from starfish.agent.memory_agent import MemoryAgent
from starfish.asset.memory_asset import MemoryAsset

TEST_DOWNLOAD_PATH = tempfile.gettempdir()
VALID_DID = 'did:op:' + secrets.token_hex(64)
INVALID_DID = 'did:ox:' + secrets.token_hex(128)


def _register_asset(ocean, metadata, config):
    account = ocean.get_account(config.accounts[0].as_dict)
    agent = MemoryAgent(ocean)
    assert(agent)
    asset = MemoryAsset(metadata)
    assert(asset)
    listing = agent.register_asset(asset, account)
    return (listing, agent, asset)

def _purchase_asset(ocean, metadata, config):
    listing, agent, asset = _register_asset(ocean, metadata, config)
    account = ocean.get_account(config.accounts[1].as_dict)
    purchase = agent.purchase_asset(listing, account)
    return purchase, listing, agent, asset, account

def test_init(ocean):
    agent = MemoryAgent(ocean)
    assert(agent)

def test_register_asset(ocean, metadata, config):
    listing, agent, asset = _register_asset(ocean, metadata, config)
    assert(listing)
    assert(listing.listing_id)

def test_get_listing(ocean, metadata, config):
    listing, agent, asset = _register_asset(ocean, metadata, config)
    found_listing = agent.get_listing(listing.listing_id)
    assert(found_listing)
    assert(found_listing.listing_id == listing.listing_id)

def test_search_listings(ocean, metadata, config):
    listing, agent, asset = _register_asset(ocean, metadata, config)
    listing_ids = agent.search_listings(metadata['base']['author'])
    assert(listing_ids)
    assert(len(listing_ids) > 0)
    is_found = False
    for listing_id in listing_ids:
        if listing_id == listing.listing_id:
            is_found = True
            break
    assert(is_found)

def test_purchase_asset(ocean, metadata, config):
    listing, agent, asset = _register_asset(ocean, metadata, config)
    account = ocean.get_account(config.accounts[1].as_dict)
    purchase = agent.purchase_asset(listing, account)
    assert(purchase)


def test_is_access_granted_for_asset(ocean, metadata, config):
    purchase, listing, agent, asset, account = _purchase_asset(ocean, metadata, config)
    assert(agent.is_access_granted_for_asset(asset, purchase.purchase_id, account))

def test_consume_asset(ocean, metadata, config):
    purchase, listing, agent, asset, account = _purchase_asset(ocean, metadata, config)
    assert(agent.consume_asset(listing, purchase.purchase_id, account, TEST_DOWNLOAD_PATH))

def test_is_did_valid():
    assert(MemoryAgent.is_did_valid(VALID_DID))
    # FIXME: This should be invalid
    assert( MemoryAgent.is_did_valid(INVALID_DID))
