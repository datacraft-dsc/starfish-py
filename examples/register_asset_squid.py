#!/usr/bin/env python3

from starfish import Ocean
from starfish.asset import RemoteDataAsset
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
    'account': ('0x00bd138abd70e2f00903268f3db08f2d25677c9e', 'node0', 'tests/resources/account_key_files/key_file_2.json')
}

NILE_CONFIG = {
    'keeper_url': 'https://nile.dev-ocean.com',
    'squid_agent': {
        'aquarius_url': 'https://aquarius.nile.dev-ocean.com',
        'brizo_url': 'https://brizo.nile.dev-ocean.com',
        'secret_store_url': 'https://secret-store.dev-ocean.com',
        'parity_url': 'https://nile.dev-ocean.com',
        'storage_path': 'squid_py.db',
    },
    'account': ('0x413c9ba0a05b8a600899b41b0c62dd661e689354', 'ocean_secret'),
}

CONFIG = LOCAL_CONFIG

def main():

    # Create a new Ocean instance.
    ocean = Ocean(keeper_url=CONFIG['keeper_url'])

    print('config data', CONFIG)
    account = ocean.load_account(CONFIG['account'])

    # Print out the account's ocean balance.
    print('my account ocean balance:', account.ocean_balance)
    print('my account ether balance:', account.ether_balance)

    # create a listing specifying the information about the asset
    listing_data = {
        'name': 'The white paper',
        'author': 'Ocean Protocol',
        'license': 'CC0: Public Domain',
        'price': '10'
    }
    # Now create a squid asset using a test URL
    asset = RemoteDataAsset.create_with_url('my test asset', 'https://oceanprotocol.com/tech-whitepaper.pdf')


    # Create a new `Squid` agent to do the work on the block chain.
    agent = SquidAgent(ocean, CONFIG['squid_agent'])

    # Register the asset, on the block chain.
    listing = agent.register_asset_and_listing(asset, listing_data, account)

    # Print out the listing did and listing data.
    print('the listing', listing.did, listing.data)

if __name__ == '__main__':
    main()
