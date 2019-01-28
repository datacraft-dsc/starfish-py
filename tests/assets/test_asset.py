"""
    Test ocean class

"""

import pathlib
import json
import logging
import time
from web3 import Web3

from ocean_py.ocean import Ocean
from ocean_py.logging import setup_logging
from ocean_py import logger

from squid_py.service_agreement.service_factory import ServiceDescriptor
from squid_py.utils.utilities import generate_new_id
from squid_py import ACCESS_SERVICE_TEMPLATE_ID
from squid_py.keeper.event_listener import EventListener

from squid_py.brizo.brizo import Brizo
from tests.helpers.brizo_mock import BrizoMock


setup_logging(level=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("web3").setLevel(logging.WARNING)

CONFIG_PARMS = {
    'contracts_path': 'artifacts',
    'keeper_url': 'http://localhost:8545',
    'secret_store_url': 'http://localhost:12001',
    'parity_url': 'http://localhost:8545',
    'parity_address': '0x00bd138abd70e2f00903268f3db08f2d25677c9e',
    'parity_password': 'node0',
}


METADATA_SAMPLE_PATH = pathlib.Path.cwd() / 'tests' / 'resources' / 'metadata' / 'sample_metadata1.json'


def _log_event(event_name):
    def _process_event(event):
        logging.debug(f'Received event {event_name}: {event}')
    return _process_event

def test_asset():
    # create an ocean object
    ocean = Ocean(CONFIG_PARMS)
    assert ocean
    assert ocean.accounts


    # test node has the account #0 unlocked
    publisher_account = ocean.accounts[list(ocean.accounts)[0]]
    publisher_account.password = ocean.config.parity_password
    publisher_account.unlock()
    publisher_account.request_tokens(10)

    # load in the sample metadata
    assert METADATA_SAMPLE_PATH.exists(), "{} does not exist!".format(METADATA_SAMPLE_PATH)
    metadata = None
    with open(METADATA_SAMPLE_PATH, 'r') as file_handle:
        metadata = json.load(file_handle)
    assert metadata

    # as of squid-0.1.22 - price is set in the metadata
    #service_descriptors = [ServiceDescriptor.access_service_descriptor(asset_price)]


    asset = ocean.register_asset(metadata, account=publisher_account)
    assert asset
    assert asset.did

    asset_did = asset.did
    # start to test getting the asset from storage
    asset = ocean.get_asset(asset_did)
    assert asset
    assert asset.did == asset_did


    purchase_account = ocean.accounts[list(ocean.accounts)[1]]

    # TODO: have this password saved in config or even better a wallet.
    purchase_account.password = 'secret'
    purchase_account.unlock()

    purchase_account.request_tokens(4)

    # since Brizo does not work outside in the barge , we need to start
    # brizo as a dumy client to do the brizo work...
    Brizo.set_http_client(BrizoMock(ocean.squid, publisher_account))

    # test purchase an asset
    purchase_asset = asset.purchase(purchase_account)
    assert purchase_asset


    filter1 = {'serviceAgreementId': Web3.toBytes(hexstr=purchase_asset.purchase_id)}
    filter2 = {'serviceId': Web3.toBytes(hexstr=purchase_asset.purchase_id)}

    EventListener('ServiceAgreement', 'ExecuteAgreement', filters=filter1).listen_once(
        _log_event('ExecuteAgreement'),
        10,
        blocking=True
    )
    EventListener('AccessConditions', 'AccessGranted', filters=filter2).listen_once(
        _log_event('AccessGranted'),
        10,
        blocking=True
    )
    event = EventListener('ServiceAgreement', 'AgreementFulfilled', filters=filter1).listen_once(
        _log_event('AgreementFulfilled'),
        10,
        blocking=True
    )

    assert purchase_asset.is_purchased
    assert not asset.is_purchased
    assert purchase_asset.is_purchase_valid(purchase_account)

    purchase_asset.consume(purchase_account)
