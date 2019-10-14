#!/usr/bin/env python3

from starfish import Ocean
from starfish.asset import DataAsset
from starfish.agent import RemoteAgent

def main():

    # Create a new Ocean instance.
    ocean = Ocean(keeper_url='http://localhost:8545')

    # Now create a memory asset
    asset = DataAsset.create('TestAsset', 'Some test data that I want to save for this asset')

    # Print the asset data
    print('my asset:', asset.data)

    # Create a remote agent to do the work.
    agent_url = 'http://localhost:8080'
    agent_ddo = RemoteAgent.generate_ddo(agent_url)
    agent_options = {
        'url': agent_url,
        'username': 'test',
        'password':  'foobar',
    }

    # create a listing specifying the information about the asset
    listing_data = {
        'name': 'The white paper',
        'author': 'Ocean Protocol',
        'license': 'CC0: Public Domain',
        'price': '0'
    }
    agent = RemoteAgent(ocean, ddo=agent_ddo, options=agent_options)

    listing = agent.register_asset(asset, listing_data)
    print(listing.did, listing.data)

    # now upload the asset data to Surfer
    agent.upload_asset(asset)

if __name__ == '__main__':
    main()
