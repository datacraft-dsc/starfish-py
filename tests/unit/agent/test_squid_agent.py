
import pytest
import secrets
import tempfile


from starfish.agent.squid_agent import SquidAgent
from starfish.asset.asset import Asset
from starfish.exceptions import StarfishPurchaseError

from tests.unit.mocks.mock_squid_model import MockSquidModel


TEST_DOWNLOAD_PATH = tempfile.gettempdir()
VALID_DID = 'did:op:' + secrets.token_hex(64)
INVALID_DID = 'did:ox:' + secrets.token_hex(128)
TEST_INIT_PARMS = {
    'aquarius_url': 'http://test_aquarius:5000',
    'brizo_url': 'http://test_brizo:8030',
    'secret_store_url': 'http://test_secret_store_url:12001',
    'storage_path': 'test_squid_path',
}

def _register_asset(ocean, metadata, config):
    account = ocean.get_account(config.accounts[0].as_dict)
    agent = SquidAgent(ocean)
    assert(agent)
    asset = Asset(metadata)
    assert(asset)
    listing = agent.register_asset(asset, account)
    return (listing, agent, asset)

def _purchase_asset(ocean, metadata, config):
    listing, agent, asset = _register_asset(ocean, metadata, config)
    account = ocean.get_account(config.accounts[1].as_dict)
    purchase = agent.purchase_asset(listing, account)
    return purchase, listing, agent, asset, account

def test_init(ocean):

    agent = SquidAgent(ocean, TEST_INIT_PARMS)
    assert(agent)
    assert isinstance(agent.squid_model, MockSquidModel)
    assert(agent.squid_model.options['aquarius_url'] == TEST_INIT_PARMS['aquarius_url'])
    assert(agent.squid_model.options['brizo_url'] == TEST_INIT_PARMS['brizo_url'])
    assert(agent.squid_model.options['secret_store_url'] == TEST_INIT_PARMS['secret_store_url'])
    assert(agent.squid_model.options['storage_path'] == TEST_INIT_PARMS['storage_path'])

    agent = SquidAgent(ocean,
        aquarius_url = TEST_INIT_PARMS['aquarius_url'],
        brizo_url = TEST_INIT_PARMS['brizo_url'],
        secret_store_url = TEST_INIT_PARMS['secret_store_url'],
        storage_path = TEST_INIT_PARMS['storage_path']
    )
    assert(agent)
    assert(agent.squid_model.options['aquarius_url'] == TEST_INIT_PARMS['aquarius_url'])
    assert(agent.squid_model.options['brizo_url'] == TEST_INIT_PARMS['brizo_url'])
    assert(agent.squid_model.options['secret_store_url'] == TEST_INIT_PARMS['secret_store_url'])
    assert(agent.squid_model.options['storage_path'] == TEST_INIT_PARMS['storage_path'])

def test_register_asset(ocean, metadata, config):
    listing, agent, asset = _register_asset(ocean, metadata, config)
    assert(listing)
    assert(listing.listing_id)

def test_validate_asset(ocean, metadata):
    agent = SquidAgent(ocean, TEST_INIT_PARMS)
    assert(agent)
    asset = Asset(metadata)
    assert(agent.validate_asset(asset))

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

def test_purchase_wait_for_completion(ocean, metadata, config):
    purchase, listing, agent, asset, account = _purchase_asset(ocean, metadata, config)
    assert(agent.purchase_wait_for_completion(purchase.purchase_id, 30))
    # test raised error if purchase failed
    with pytest.raises(StarfishPurchaseError):
        agent.purchase_wait_for_completion(None, 30)

def test_consume_asset(ocean, metadata, config):
    purchase, listing, agent, asset, account = _purchase_asset(ocean, metadata, config)
    assert(agent.consume_asset(listing, purchase.purchase_id, account, TEST_DOWNLOAD_PATH))

def test_is_did_valid():
    assert(SquidAgent.is_did_valid(VALID_DID))
    # FIXME: This should be invalid
    assert( SquidAgent.is_did_valid(INVALID_DID))
