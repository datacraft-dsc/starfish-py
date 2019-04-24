"""
    Test invoke agent

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
from squid_py.brizo.brizo_provider import BrizoProvider
from squid_py.brizo.brizo import Brizo
from tests.integration.mocks.brizo_mock import BrizoMock
import requests
import hashlib
from starfish import (
    Ocean,
    logger
)
from starfish.agent.invoke_agent import InvokeAgent


def _register_asset_for_sale(agent, metadata, account):
    asset = SquidAsset(metadata)
    listing = agent.register_asset(asset, account=account)
    assert listing
    assert listing.asset.did
    return listing

def purchase_asset(ocean, metadata, config):


    agent = SquidAgent(ocean, config.squid_config)
    assert agent


    # test node has the account #0 unlocked
    publisher_account = ocean.get_account(config.publisher_account)
    publisher_account.unlock()
    publisher_account.request_tokens(20)

    listing = _register_asset_for_sale(agent, metadata, publisher_account)
    assert listing
    assert publisher_account

    listing_did = listing.asset.did
    # start to test getting the asset from storage
    listing = agent.get_listing(listing_did)
    assert listing
    assert listing.asset.did == listing_did
    ld=listing.data
    logging.info(f' listing.data is {ld}')
    purchase_account = ocean.get_account(config.purchaser_account)
    logging.info(f'purchase_account {purchase_account.ocean_balance}')

    purchase_account.unlock()

    purchase_account.request_tokens(10)

    time.sleep(2)
    logging.info(f'purchase_account after token request {purchase_account.ocean_balance}')

    # since Brizo does not work outside in the barge , we need to start
    # brizo as a dumy client to do the brizo work...
    model = SquidModel(ocean)
    BrizoMock.ocean_instance = model.get_squid_ocean()
    BrizoMock.publisher_account = publisher_account._squid_account
    BrizoProvider.set_brizo_class(BrizoMock)


    # test purchase an asset
    purchase_asset = listing.purchase(purchase_account)
    assert purchase_asset

    assert(not purchase_asset.is_completed(purchase_account))

    error_message = purchase_asset.wait_for_completion()
    assert(error_message == True)

    assert(purchase_asset.is_completed(purchase_account))

    assert purchase_asset.is_purchased
    assert purchase_asset.is_purchase_valid(purchase_account)
    return purchase_asset.purchase_id,listing_did


def test_invoke_with_sa(ocean, metadata, config):

    said,did=purchase_asset(ocean, metadata, config)
    assert said
    agent = InvokeAgent()
    assert agent

    res=agent.get_operations()
    assert 'hashing_did'==res['hashing']

    op=agent.get_operation('hashing_did')
    assert op

    sch=op.get_schema()
    assert 1==len(sch)
    assert sch['to_hash']=='asset'
    url='http://samplecsvs.s3.amazonaws.com/Sacramentorealestatetransactions.csv'
    download = requests.get(url)
    m = hashlib.sha256()
    m.update(download.content)
    hashval= m.hexdigest()

    res=op.invoke(to_hash={'serviceAgreementId':said,
        'did':did,
        'url':url,
        'consumerAddress':config.purchaser_account['address']})
    logging.info(f' invoke returns {res}')
    # TO DO: This needs testing again, since koi fails on calling invoke in the current barge.
    # assert res['hash']==hashval
