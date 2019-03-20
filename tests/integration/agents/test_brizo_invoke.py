"""
    Test ocean class

"""

import pathlib
import json
import logging
import time
from web3 import Web3

from starfish import Ocean
from starfish.models.squid_model import SquidModel
from starfish.agent import SquidAgent
from starfish.asset import SquidAsset

from starfish.logging import setup_logging

from squid_py.agreements.service_factory import ServiceDescriptor
from squid_py.utils.utilities import generate_new_id
from squid_py.agreements.service_types import ACCESS_SERVICE_TEMPLATE_ID
from squid_py.keeper.event_listener import EventListener
from squid_py.brizo.brizo_provider import BrizoProvider

from tests.integration.helpers.koi_mock import KoiMock

CONFIG_PARAMS = {'contracts_path': 'artifacts', 'keeper_url': 'http://localhost:8545'}

PUBLISHER_ACCOUNT = { 'address': '0x00bd138abd70e2f00903268f3db08f2d25677c9e', 'password': 'node0'}
PURCHASER_ACCOUNT = {'address': '0x068Ed00cF0441e4829D9784fCBe7b9e26D4BD8d0', 'password': 'secret'}

SQUID_AGENT_CONFIG_PARAMS = {
    'aquarius_url': 'http://localhost:5000',
    'brizo_url': 'http://localhost:8031',
    'secret_store_url': 'http://localhost:12001',
    'parity_url': 'http://localhost:9545',
    'storage_path': 'squid_py.db',
}
SQUID_DOWNLOAD_PATH = 'consume_downloads'

METADATA_SAMPLE_PATH = pathlib.Path.cwd() / 'tests' / 'resources' / 'metadata' / 'invoke_metadata.json'

def _read_metadata():
    # load in the sample metadata
    assert METADATA_SAMPLE_PATH.exists(), "{} does not exist!".format(METADATA_SAMPLE_PATH)
    metadata = None
    with open(METADATA_SAMPLE_PATH, 'r') as file_handle:
        metadata = json.load(file_handle)

    return metadata

def _register_asset_for_sale(agent, account):


    metadata = _read_metadata()
    assert metadata

    asset=SquidAsset(metadata)
    listing = agent.register_asset(asset, account=account)
    assert listing
    assert listing.asset.did
    return listing

def _log_event(event_name):
    def _process_event(event):
        logging.debug(f'Received event {event_name}: {event}')
    return _process_event

def test_invoke():

    # create an ocean object
    ocean = Ocean(CONFIG_PARAMS, log_level=logging.DEBUG)
    assert ocean
    assert ocean.accounts

    agent = SquidAgent(ocean, SQUID_AGENT_CONFIG_PARAMS)
    assert agent


    # test node has the account #0 unlocked
    publisher_account = ocean.get_account(PUBLISHER_ACCOUNT)
    publisher_account.unlock()
    publisher_account.request_tokens(20)

    # check to see if the sla template has been registered, this is only run on
    agent.init_network(publisher_account)

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

    #Use the Koi server, and therefore use the Koi client instead of Brizo.py
    model = agent.squid_model
    KoiMock.ocean_instance = model.get_squid_ocean()
    KoiMock.publisher_account = publisher_account._squid_account
    BrizoProvider.set_brizo_class(KoiMock)

    # test purchase an asset
    # this purchase does not automatically fire a consume() request as no callback is registered
    purchase_asset = listing.purchase(purchase_account)
    assert purchase_asset


    _filter = {'agreementId': Web3.toBytes(hexstr=purchase_asset.purchase_id)}
    pid=purchase_asset.purchase_id
    logging.info(f' invoke test purchase id {pid}')
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
    #assert purchase_asset.is_purchase_valid(purchase_account)
    #this assertion fails
    purch_type=purchase_asset.get_type
    logging.debug(f'purchase type {purch_type}')
    paramvalue={'hello':'world'}
    result=purchase_asset.invoke(purchase_account,{'operation':'echo','params':paramvalue})
    ## TBD: asset on the result of the invoke
    logging.debug(f'invoke result {result}')
    assert result == paramvalue


#test_asset()
