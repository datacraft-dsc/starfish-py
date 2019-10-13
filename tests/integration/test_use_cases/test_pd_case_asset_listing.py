"""
    test_pd_case_search_listings

    As a developer
    I want register an asset in squid, and then find it in the search listings,

"""

import secrets
import logging
import json
from web3 import Web3

from starfish.asset import (
    DataAsset,
    RemoteDataAsset,
)

def test_pd_case_file_transfer(ocean, config, resources, remote_agent, squid_agent, publisher_account):

    # for the use case , we need to assign a unique id to the asset
    # so we know that it's from the publisher
    pd_test_case_tag = 'pd_test_case'
    unique_pd_case_id = secrets.token_hex(32)
    dummy_did = secrets.token_hex(32)
    dummy_asset_id = secrets.token_hex(32)
    # create a pretend dummy url based on the dummy remote agent DID & dummy asset_id saved in remote agent
    dummy_url = 'op:did:{dummy_did}/{dummy_asset_id}'

    # now create a checksum so that we know this actually comes from the correct publisher
    valid_check = Web3.toHex(Web3.sha3(text=f'{unique_pd_case_id}{dummy_url}{publisher_account.address}'))

    listing_data = {
        'name': 'Test file asset',
        'description': 'Test asset for sale - not for public purchase',
        'author': 'pd_test_case asset listing',
        'license': 'Closed',
        'price': 3.141592,
        'extra_data': {
            'id': unique_pd_case_id,
            'valid_check': valid_check,
        },
        'tags': [pd_test_case_tag],
    }
    asset_sale = RemoteDataAsset.create_with_url('TestAsset', dummy_url)
    # print('metadata ',squid_agent._convert_listing_asset_to_metadata(asset_sale, listing_data))

    listing = squid_agent.register_asset(asset_sale, listing_data, account=publisher_account)
    assert(listing)

    listing_items = squid_agent.search_listings({'tags': [pd_test_case_tag]})

    assert(len(listing_items) >= 1)
    for listing in listing_items:
        assert('tags' in listing.data and pd_test_case_tag in listing.data['tags'])
        assert(listing.data['extra_data'])
        assert(isinstance(listing.data['extra_data'], dict))
        if listing.data['extra_data']['id'] == unique_pd_case_id:
            assert(listing.data['extra_data']['valid_check'] == valid_check)
