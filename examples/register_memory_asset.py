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

    # create a new test account to register
    register_account = ocean.create_account('any old password')

    # print the new account
    print('my new register account', register_account)

    # Now create a memory asset
    asset = MemoryAsset(data='Some test data that I want to save for this asset')

    # Print the memory asset out
    print('my asset:', asset.data)

    # Create a new memory agent to do the work.
    agent = MemoryAgent(ocean)

    # Register the memory asset, with the new account.
    listing = agent.register_asset(asset, register_account)

    # Print out the listing did and listing data.
    print('memory listing', listing.listing_id, listing.data)


if __name__ == '__main__':
    main()
