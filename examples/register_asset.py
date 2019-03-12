#!/usr/bin/env python3

import json
import pathlib

from starfish import Ocean
from starfish.asset import SquidAsset
from starfish.agent import SquidAgent


"""

The full set of parameters needed to access the 'ocean' network servers
and configuration information.

"""
SQUID_AGENT_CONFIG_PARAMS = {
    'aquarius_url': 'http://localhost:5000',
    'brizo_url': 'http://localhost:8030',
    'secret_store_url': 'http://localhost:12001',
    'parity_url': 'http://localhost:9545',
    'storage_path': 'squid_py.db',
}

"""
Test sample metadata to load in for an asset.
"""
METADATA_SAMPLE_PATH = pathlib.Path.cwd() / 'examples' / 'sample_data' / 'sample_metadata.json'

def read_sample_metadata():
    """
    Reads the sample metadata from the 'sample_data' folder within the examples.
    """
    if not METADATA_SAMPLE_PATH.exists():
        print(f'{METADATA_SAMPLE_PATH} does not exist!')
        return None

    metadata = None
    with open(METADATA_SAMPLE_PATH, 'r') as file_handle:
        metadata = json.load(file_handle)

    return metadata

def main():
    """ Create a new Ocean instance. logging information. """
    ocean = Ocean(contracts_path='artifacts', keeper_url='http://localhost:8545')
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
    account = ocean.get_account('0x00bd138abd70e2f00903268f3db08f2d25677c9e', 'node0')

    """ Print out the account's ocean balance. """
    print('my account ocean balance:', account.ocean_balance)
    print('my account ether balance:', account.ether_balance)

    """ Load in our sample metadata """
    metadata = read_sample_metadata()

    """ Now create a squid asset using the metadata we have just loaded """
    asset = SquidAsset(metadata)

    """ Print the squid asset out. """
    print('my asset:', asset.metadata)

    """ Create a new `Squid` agent to do the work on the block chain. """
    agent = SquidAgent(ocean, SQUID_AGENT_CONFIG_PARAMS)

    """ Register the asset, on the block chain and with the metadata storage. """
    listing = agent.register_asset(asset, account)

    """ Print out the listing did and listing data. """
    print('the listing', listing.did, listing.data)

if __name__ == '__main__':
    main()
