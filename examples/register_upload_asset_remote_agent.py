#!/usr/bin/env python3

from starfish.network.convex.convex_network import ConvexNetwork
from starfish.asset import DataAsset
from starfish.agent import RemoteAgent

def main():

    # Create a new convex network instance.
    network = ConvexNetwork('https://convex.world')

    # Create a remote agent to do the work.
    agent_url = 'http://localhost:3030'

    authentication = {
        'username': 'Aladdin',
        'password':  'OpenSesame',
    }

    # find an agent based on it's url, you can also use an agent did or asset did instead
    agent = RemoteAgent.load(agent_url, network, authentication=authentication)
    if not agent:
        print('failed to find the agent')

    # create a listing specifying the information about the asset
    listing_data = {
        'name': 'The white paper',
        'author': 'Ocean Protocol',
        'license': 'CC0: Public Domain',
        'price': '0'
    }

    # Now create a memory asset
    asset = DataAsset.create('TestAsset', 'Some test data that I want to save for this asset')

    asset.add_provenance_publish(agent.did)

    # Print the asset data
    print('my asset:', asset.data)

    asset = agent.register_asset(asset)
    print(asset.did)
    listing = agent.create_listing(listing_data, asset.did)
    print(listing.did, listing.data)

    # now upload the asset data to Surfer
    agent.upload_asset(asset)

if __name__ == '__main__':
    main()
