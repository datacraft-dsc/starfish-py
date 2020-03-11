#!/usr/bin/env python3

from starfish import DNetwork
from starfish.asset import DataAsset
from starfish.agent import RemoteAgent
from starfish.agent.services import Services

def main():

    # Create a new Ocean instance.
    network = DNetwork()
    network.connect('http://localhost:8545')
    print(network.name)

    # Now create a memory asset
    asset = DataAsset.create('TestAsset', 'Some test data that I want to save for this asset')

    # Print the asset data
    print('my asset:', asset.data)

    # Create a remote agent to do the work.
    agent_url = 'http://localhost:3030'
    services = Services(agent_url, all_services=True)
    agent_ddo = RemoteAgent.generate_ddo(services)
    agent_options = {
        'url': agent_url,
        'username': 'Aladdin',
        'password':  'OpenSesame',
    }

    # create a listing specifying the information about the asset
    listing_data = {
        'name': 'The white paper',
        'author': 'Ocean Protocol',
        'license': 'CC0: Public Domain',
        'price': '0'
    }
    agent = RemoteAgent(network, ddo=agent_ddo, options=agent_options)

    asset = agent.register_asset(asset)
    print(asset.did)
    listing = agent.create_listing(listing_data, asset.did)
    print(listing.did, listing.data)

    # now upload the asset data to Surfer
    agent.upload_asset(asset)

if __name__ == '__main__':
    main()
