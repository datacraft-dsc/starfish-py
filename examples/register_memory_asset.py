#!/usr/bin/env python3


from starfish import Ocean
from starfish.asset import MemoryAsset
from starfish.agent import MemoryAgent


def main():
    """
    Create a new Ocean instance.
    You can pass 'log_level=logging.DEBUG' parameter to get full debug
    logging information.
    """
    ocean = Ocean()

    # test account to regisetr

    register_account = ocean.create_account('any old password')
    # Now create a memory asset
    asset = MemoryAsset(data='Some test data that I want to save for this asset')

    # Print the memory asset out
    print('my asset:', asset.data)

    # Create a new memory agent to do the work.
    agent = MemoryAgent(ocean)

    # Register the memory asset.
    listing = agent.register_asset(asset, register_account)

    # Print out the listing did and listing data.
    print('memory listing', listing.did, listing.data)


if __name__ == '__main__':
    main()
