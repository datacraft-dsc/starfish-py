
import datetime
import pytest
import secrets
import tempfile
import math


from starfish.agent.squid_agent import SquidAgent
from starfish.asset import (
    BundleAsset,
    DataAsset,
    RemoteDataAsset,
)
from starfish.exceptions import StarfishPurchaseError
from tests.unit.mocks.mock_squid_agent_adapter import MockSquidAgentAdapter


VALID_DID = 'did:op:' + secrets.token_hex(64)
INVALID_DID = 'did:ox:' + secrets.token_hex(128)
TEST_INIT_PARMS = {
    'aquarius_url': 'http://test_aquarius:5000',
    'brizo_url': 'http://test_brizo:8030',
    'secret_store_url': 'http://test_secret_store_url:12001',
    'storage_path': 'test_squid_path',
}

def _register_asset(ocean, resources, config):
    account = ocean.load_account(config.accounts[0].as_dict)
    agent = SquidAgent(ocean)
    assert(agent)
    asset = RemoteDataAsset.create_with_url('test url asset', resources.asset_remote)
    assert(asset)
    listing = agent.register_asset(asset, resources.listing_data, account)
    return (listing, agent, asset)

def _purchase_asset(ocean, resources, config):
    listing, agent, asset = _register_asset(ocean, resources, config)
    account = ocean.load_account(config.accounts[1].as_dict)
    purchase = agent.purchase_asset(listing, account)
    return purchase, listing, agent, asset, account

def test_init(ocean):

    agent = SquidAgent(ocean, TEST_INIT_PARMS)
    assert(agent)
    assert isinstance(agent.agent_adapter, MockSquidAgentAdapter)
    adapter = agent.agent_adapter
    assert(adapter.options['aquarius_url'] == TEST_INIT_PARMS['aquarius_url'])
    assert(adapter.options['brizo_url'] == TEST_INIT_PARMS['brizo_url'])
    assert(adapter.options['secret_store_url'] == TEST_INIT_PARMS['secret_store_url'])
    assert(adapter.options['storage_path'] == TEST_INIT_PARMS['storage_path'])

    agent = SquidAgent(ocean,
        aquarius_url = TEST_INIT_PARMS['aquarius_url'],
        brizo_url = TEST_INIT_PARMS['brizo_url'],
        secret_store_url = TEST_INIT_PARMS['secret_store_url'],
        storage_path = TEST_INIT_PARMS['storage_path']
    )
    assert(agent)
    adapter = agent.agent_adapter
    assert(adapter)
    assert(adapter.options['aquarius_url'] == TEST_INIT_PARMS['aquarius_url'])
    assert(adapter.options['brizo_url'] == TEST_INIT_PARMS['brizo_url'])
    assert(adapter.options['secret_store_url'] == TEST_INIT_PARMS['secret_store_url'])
    assert(adapter.options['storage_path'] == TEST_INIT_PARMS['storage_path'])

def test_register_asset(ocean, resources, config):
    listing, agent, asset = _register_asset(ocean, resources, config)
    assert(listing)
    assert(listing.listing_id)

def test_register_bundle_asset(ocean, resources, config):
    account = ocean.load_account(config.accounts[0].as_dict)
    agent = SquidAgent(ocean)
    assert(agent)
    bundle_asset = BundleAsset.create('test bundle asset')
    for index in range(0, 5):
        asset = RemoteDataAsset.create_with_url('test remote asset', resources.asset_remote)
        assert(asset)
        bundle_asset.add(f'name_{index}', asset)
    listing = agent.register_asset(bundle_asset, resources.listing_data, account)
    assert(listing)

def test_register_asset_invalid_data(ocean, resources, config):
    account = ocean.load_account(config.accounts[0].as_dict)
    agent = SquidAgent(ocean)
    assert(agent)
    asset = DataAsset.create('test remote asset', 'some data that is never going to be saved')
    with pytest.raises(ValueError):
        listing = agent.register_asset(asset, resources.listing_data, account)

def test_validate_asset(ocean):
    agent = SquidAgent(ocean, TEST_INIT_PARMS)
    assert(agent)
    asset = RemoteDataAsset.create_with_url('TestAsset', 'http://dex.sg')
    assert(agent.validate_asset(asset))

def test_get_listing(ocean, resources, config):
    listing, agent, asset = _register_asset(ocean, resources, config)
    found_listing = agent.get_listing(listing.listing_id)
    assert(found_listing)
    assert(found_listing.listing_id == listing.listing_id)

def test_search_listings(ocean, resources, config):
    listing, agent, asset = _register_asset(ocean, resources, config)
    listing_items = agent.search_listings(resources.listing_data['author'])
    assert(listing_items)
    assert(len(listing_items) > 0)
    is_found = False
    listing_id = listing.listing_id
    for listing in listing_items:
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
    assert(agent.is_access_granted_for_asset(asset, account, purchase.purchase_id, ))

def test_purchase_wait_for_completion(ocean, resources, config):
    purchase, listing, agent, asset, account = _purchase_asset(ocean, resources, config)
    assert(agent.purchase_wait_for_completion(asset, account, purchase.purchase_id, 30))
    # test raised error if purchase failed
    with pytest.raises(ValueError):
        agent.purchase_wait_for_completion(asset, account, None, 30)

def test_consume_asset(ocean, resources, config):
    purchase, listing, agent, asset, account = _purchase_asset(ocean, resources, config)
    assert(agent.consume_asset(listing, account,  purchase.purchase_id))

def test_is_did_valid():
    assert(SquidAgent.is_did_valid(VALID_DID))
    # FIXME: This should be invalid
    assert( SquidAgent.is_did_valid(INVALID_DID))

def test_price_out_of_range(ocean, resources, config):
    account = ocean.load_account(config.accounts[0].as_dict)
    agent = SquidAgent(ocean)
    assert(agent)
    asset = RemoteDataAsset.create_with_url('test squid asset with url', resources.asset_remote)
    assert(asset)
    resources.listing_data['price'] = -1
    with pytest.raises(ValueError):
        listing = agent.register_asset(asset, resources.listing_data, account)
    resources.listing_data['price'] = math.pow(2, 197)
    with pytest.raises(ValueError):
        listing = agent.register_asset(asset, resources.listing_data, account)
