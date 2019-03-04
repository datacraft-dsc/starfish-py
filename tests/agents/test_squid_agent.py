"""
    Test ocean class

"""

import pathlib
import json
import logging
import time
from web3 import Web3

from starfish import (
    Ocean,
    logger
)
from starfish.models.squid_model import SquidModel
from starfish.agent import SquidAgent
from starfish.asset import SquidAsset

from starfish.logging import setup_logging

from squid_py.agreements.service_factory import ServiceDescriptor
from squid_py.utils.utilities import generate_new_id
from squid_py.agreements.service_types import ACCESS_SERVICE_TEMPLATE_ID
from squid_py.keeper.event_listener import EventListener
from squid_py.brizo.brizo_provider import BrizoProvider
from squid_py.brizo.brizo import Brizo

from tests.helpers.brizo_mock import (
    BrizoMock,
    brizo_mock_ocean_instance,
    brizo_mock_account
)


setup_logging(level=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("web3").setLevel(logging.WARNING)

CONFIG_PARAMS = {'contracts_path': 'artifacts', 'keeper_url': 'http://localhost:8545' }

PUBLISHER_ACCOUNT = { 'address': '0x00bd138abd70e2f00903268f3db08f2d25677c9e', 'password': 'node0'}
PURCHASER_ACCOUNT = {'address': '0x068Ed00cF0441e4829D9784fCBe7b9e26D4BD8d0', 'password': 'secret'}

SQUID_AGENT_CONFIG_PARAMS = {
    'aquarius_url': 'http://localhost:5000',
    'brizo_url': 'http://localhost:8030',
    'secret_store_url': 'http://localhost:12001',
    'parity_url': 'http://localhost:9545',
    'storage_path': 'squid_py.db',
}
SQUID_DOWNLOAD_PATH = 'consume_downloads'

METADATA_SAMPLE_PATH = pathlib.Path.cwd() / 'tests' / 'resources' / 'metadata' / 'sample_metadata1.json'

def _read_metadata():
    # load in the sample metadata
    assert METADATA_SAMPLE_PATH.exists(), "{} does not exist!".format(METADATA_SAMPLE_PATH)
    metadata = None
    with open(METADATA_SAMPLE_PATH, 'r') as file_handle:
        metadata = json.load(file_handle)

    return metadata

def _create_asset():
    metadata = _read_metadata()
    assert metadata
    return SquidAsset(metadata)

def _register_asset_for_sale(agent, account):
    asset = _create_asset()
    listing = agent.register_asset(asset, account=account)
    assert listing
    assert listing.asset.did
    return listing

def _log_event(event_name):
    def _process_event(event):
        logging.debug(f'Received event {event_name}: {event}')
    return _process_event

def test_asset():

    # create an ocean object
    ocean = Ocean(CONFIG_PARAMS)
    assert ocean
    assert ocean.accounts

    agent = SquidAgent(ocean, SQUID_AGENT_CONFIG_PARAMS)
    assert agent


    # test node has the account #0 unlocked
    publisher_account = ocean.get_account(PUBLISHER_ACCOUNT)
    publisher_account.unlock()
    publisher_account.request_tokens(20)

    # check to see if the sla template has been registered, this is only run on
    # new networks, especially during a travis test run..
    model = SquidModel(ocean)
    if not model.is_service_agreement_template_registered(ACCESS_SERVICE_TEMPLATE_ID):
        model.register_service_agreement_template(ACCESS_SERVICE_TEMPLATE_ID, publisher_account._squid_account)



    listing = _register_asset_for_sale(agent, publisher_account)
    assert listing
    assert publisher_account

    listing_did = listing.asset.did
    # start to test getting the asset from storage
    listing = agent.get_listing(listing_did)
    assert listing
    assert listing.asset.did == listing_did


    purchase_account = ocean.get_account(PURCHASER_ACCOUNT)
    logging.info(f'purchase_account {purchase_account.ocean_balance}')

    purchase_account.unlock()

    purchase_account.request_tokens(10)

    time.sleep(2)
    logging.info(f'purchase_account after token request {purchase_account.ocean_balance}')

    # since Brizo does not work outside in the barge , we need to start
    # brizo as a dumy client to do the brizo work...
    BrizoMock.ocean_instance = model.get_squid_ocean()
    BrizoMock.publisher_account = publisher_account._squid_account
    BrizoProvider.set_brizo_class(BrizoMock)
    # Brizo.set_http_client(BrizoMock(model.get_squid_ocean(), publisher_account._squid_account))


    # test purchase an asset
    purchase_asset = listing.purchase(purchase_account)
    assert purchase_asset

    _filter = {'agreementId': Web3.toBytes(hexstr=purchase_asset.purchase_id)}

    EventListener('ServiceExecutionAgreement', 'AgreementInitialized', filters=_filter).listen_once(
        _log_event('AgreementInitialized'),
        20,
        blocking=True
    )
    EventListener('AccessConditions', 'AccessGranted', filters=_filter).listen_once(
        _log_event('AccessGranted'),
        20,
        blocking=True
    )
    event = EventListener('ServiceExecutionAgreement', 'AgreementFulfilled', filters=_filter).listen_once(
        _log_event('AgreementFulfilled'),
        20,
        blocking=True
    )

    assert event, 'No event received for ServiceAgreement Fulfilled.'
    assert Web3.toHex(event.args['agreementId']) == purchase_asset.purchase_id
    # assert len(os.listdir(consumer_ocean_instance.config.downloads_path)) == downloads_path_elements + 1

    # This test does not work with the current barge

    assert purchase_asset.is_purchased
    assert purchase_asset.is_purchase_valid(purchase_account)

    purchase_asset.consume(purchase_account, SQUID_DOWNLOAD_PATH)



def test_search_listing():

    ocean = Ocean(CONFIG_PARAMS)
    assert ocean
    assert ocean.accounts

    agent = SquidAgent(ocean, SQUID_AGENT_CONFIG_PARAMS)

    # test node has the account #0 unlocked
    publisher_account = ocean.get_account(PUBLISHER_ACCOUNT)
    publisher_account.unlock()

    listing = _register_asset_for_sale(agent, publisher_account)
    assert listing
    assert publisher_account

    metadata = _read_metadata()
    assert metadata

    # choose a word from the description field
    text = metadata['base']['description']
    words = text.split(' ')
    word = words[0]

    # should return at least 1 or more assets
    logging.info(f'search word is {word}')
    searchResult = agent.search_listings(word)
    assert searchResult

    assert(len(searchResult) > 1)
