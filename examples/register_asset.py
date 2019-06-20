#!/usr/bin/env python3

import json
import pathlib
import logging

from starfish import Ocean
from starfish.asset import RemoteAsset
from starfish.agent import SquidAgent

"""

The full set of parameters needed to access the 'ocean' network servers
and configuration information on the Nile test network.

"""

LOCAL_CONFIG = {
    'keeper_url': 'http://localhost:8545',
    'squid_agent':  {
        'aquarius_url': 'http://localhost:5000',
        'brizo_url': 'http://localhost:8030',
        'secret_store_url': 'http://localhost:12001',
        'parity_url': 'http://localhost:8545',
        'storage_path': 'squid_py.db',
    },
    'account': ('0x00bd138abd70e2f00903268f3db08f2d25677c9e', 'node0')
}

NILE_CONFIG = {
    'keeper_url': 'https://nile.dev-ocean.com',
    'squid_agent': {
        'aquarius_url': 'https://nginx-aquarius.dev-ocean.com',
        'brizo_url': 'https://nginx-brizo.dev-ocean.com',
        'secret_store_url': 'https://secret-store.dev-ocean.com',
        'parity_url': 'https://nile.dev-ocean.com',
        'storage_path': 'squid_py.db',
    },
    'account': ('0x413c9ba0a05b8a600899b41b0c62dd661e689354', 'ocean_secret'),

}

CONFIG = LOCAL_CONFIG


"""
Test sample metadata to load in for an asset.
"""
METADATA_SAMPLE_PATH = pathlib.Path.cwd() / 'examples' / 'sample_data' / 'sample_metadata.json'
MY_ACCOUNT_PASSWORD = 'test_account_password'


def main():
    """ Create a new Ocean instance. logging information. """
    
    ocean = Ocean(keeper_url=CONFIG['keeper_url'])
    
    """
    If you wish to see what's happening behind the scenes, you can pass
    'log_level=logging.DEBUG' parameter to get full debug instead.

    ocean = Ocean(contracts_path='artifacts',
                    keeper_url='http://localhost:8545',
                    log_level=logging.DEBUG
    )

    Get our first test publisher account - in test the account numbers are published
    at https://github.com/DEX-Company/barge
    """

    print('config data', CONFIG)
    account = ocean.get_account(CONFIG['account'])

    # Print out the account's ocean balance.
    print('my account ocean balance:', account.ocean_balance)
    print('my account ether balance:', account.ether_balance)

    # create a listing specifying the information about the asset
    listing_data = {
        'name': 'The white paper',
        'author': 'Ocean Protocol',
        'license': 'CC0: Public Domain',
        'price': '0'
    }
    # Now create a squid asset using the metadata we have just loaded
    asset = RemoteAsset(url='https://oceanprotocol.com/tech-whitepaper.pdf')


    # Create a new `Squid` agent to do the work on the block chain.
    agent = SquidAgent(ocean, CONFIG['squid_agent'])

    # Register the asset, on the block chain and with the metadata storage.
    listing = agent.register_asset(asset, listing_data, account)

    # Print out the listing did and listing data.
    print('the listing', listing.listing_id, listing.data)

if __name__ == '__main__':
    main()
