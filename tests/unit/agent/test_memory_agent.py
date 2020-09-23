
import datetime
import pytest
import secrets
import tempfile


from starfish.agent.memory_agent import MemoryAgent
from starfish.asset.data_asset import DataAsset
from starfish.network.ethereum_account import EthereumAccount


def create_agent():
    agent = MemoryAgent()
    assert(agent)
    return agent

def register_asset(agent):
    asset = DataAsset.create('test memory agent asset', secrets.token_bytes(1024))
    assert(asset)
    asset = agent.register_asset(asset)
    assert(asset)
    return asset

def create_listing(agent, resources, asset):
    listing = agent.create_listing(resources.listing_data, asset.did)
    assert(listing)
    return (listing)

def purchase_asset(resources, config):
    agent = create_agent()
    asset = register_asset(agent)
    listing = create_listing(agent, resources, asset)

    account = EthereumAccount.import_from_text(config.ethereum.accounts[1].key_data, config.ethereum.accounts[1].password)
    purchase = agent.purchase_asset(listing, account)
    return purchase, listing, agent, asset, account

def test_init():
    agent = MemoryAgent()
    assert(agent)

def test_register_asset(resources, config):
    agent = create_agent()
    asset = register_asset(agent)
    listing = create_listing(agent, resources, asset)
    assert(listing)
    assert(listing.listing_id)


def test_get_listing(resources, config):
    agent = create_agent()
    asset = register_asset(agent)
    listing = create_listing(agent, resources, asset)
    found_listing = agent.get_listing(listing.listing_id)
    assert(found_listing)
    assert(found_listing.listing_id == listing.listing_id)

def test_search_listings(resources, config):
    agent = create_agent()
    asset = register_asset(agent)
    listing = create_listing(agent, resources, asset)
    listing_ids = agent.search_listings(resources.listing_data['author'])
    assert(listing_ids)
    assert(len(listing_ids) > 0)
    is_found = False
    for listing_id in listing_ids:
        if listing_id == listing.listing_id:
            is_found = True
            break
    assert(is_found)

def test_purchase_asset(resources, config):
    agent = create_agent()
    asset = register_asset(agent)
    listing = create_listing(agent, resources, asset)
    account = EthereumAccount.import_from_text(config.ethereum.accounts[1].key_data, config.ethereum.accounts[1].password)
    purchase = agent.purchase_asset(listing, account)
    assert(purchase)


def test_is_access_granted_for_asset(resources, config):
    purchase, listing, agent, asset, account = purchase_asset(resources, config)
    assert(agent.is_access_granted_for_asset(asset, account, purchase.purchase_id,))

def test_consume_asset(resources, config):
    purchase, listing, agent, asset, account = purchase_asset(resources, config)
    assert(agent.consume_asset(listing, account, purchase.purchase_id,))

