
import datetime
import pytest
import secrets
import tempfile


from starfish.agent.memory_agent import MemoryAgent
from starfish.asset.data_asset import DataAsset

VALID_DID = 'did:dep:' + secrets.token_hex(64)
INVALID_DID = 'did:dep:' + secrets.token_hex(128)


def _register_asset(ocean, resources, config):
    account = ocean.load_account(config.accounts[0].as_dict)
    agent = MemoryAgent(ocean)
    assert(agent)
    asset = DataAsset.create('test memory agent asset', secrets.token_hex(1024))
    assert(asset)
    listing = agent.register_asset(asset, resources.listing_data, account)
    return (listing, agent, asset)

def _purchase_asset(ocean, resources, config):
    listing, agent, asset = _register_asset(ocean, resources, config)
    account = ocean.load_account(config.accounts[1].as_dict)
    purchase = agent.purchase_asset(listing, account)
    return purchase, listing, agent, asset, account

def test_init(ocean):
    agent = MemoryAgent(ocean)
    assert(agent)

def test_register_asset(ocean, resources, config):
    listing, agent, asset = _register_asset(ocean, resources, config)
    assert(listing)
    assert(listing.listing_id)

def test_get_listing(ocean, resources, config):
    listing, agent, asset = _register_asset(ocean, resources, config)
    found_listing = agent.get_listing(listing.listing_id)
    assert(found_listing)
    assert(found_listing.listing_id == listing.listing_id)

def test_search_listings(ocean, resources, config):
    listing, agent, asset = _register_asset(ocean, resources, config)
    listing_ids = agent.search_listings(resources.listing_data['author'])
    assert(listing_ids)
    assert(len(listing_ids) > 0)
    is_found = False
    for listing_id in listing_ids:
        if listing_id == listing.listing_id:
            is_found = True
            break
    assert(is_found)

def test_purchase_asset(ocean, resources, config):
    listing, agent, asset = _register_asset(ocean, resources, config)
    account = ocean.load_account(config.accounts[1].as_dict)
    purchase = agent.purchase_asset(listing, account)
    assert(purchase)


def test_is_access_granted_for_asset(ocean, resources, config):
    purchase, listing, agent, asset, account = _purchase_asset(ocean, resources, config)
    assert(agent.is_access_granted_for_asset(asset, account, purchase.purchase_id,))

def test_consume_asset(ocean, resources, config):
    purchase, listing, agent, asset, account = _purchase_asset(ocean, resources, config)
    assert(agent.consume_asset(listing, account, purchase.purchase_id,))

def test_is_did_valid():
    assert(MemoryAgent.is_did_valid(VALID_DID))
    # FIXME: This should be invalid
    assert( MemoryAgent.is_did_valid(INVALID_DID))
