#!/usr/bin/env python3

from starfish import Ocean
from starfish.asset import DataAsset
from starfish.agent import SurferAgent

def main():

    # Create a new Ocean instance.
    ocean = Ocean(keeper_url='http://localhost:8545')

    # Now create a memory asset
    asset = DataAsset.create('TestAsset', 'Some test data that I want to save for this asset')

    # Print the asset data
    print('my asset:', asset.data)

    # Create a surfer agent to do the work.
    surfer_url = 'http://localhost:8080'
    surfer_ddo = SurferAgent.generate_ddo(surfer_url)
    surfer_options = {
        'url': surfer_url,
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
    agent = SurferAgent(ocean, ddo=surfer_ddo, options=surfer_options)

    listing = agent.register_asset(asset, listing_data)
    print(listing.did, listing.data)

    # now upload the asset data to Surfer
    agent.upload_asset(asset)

if __name__ == '__main__':
    main()
