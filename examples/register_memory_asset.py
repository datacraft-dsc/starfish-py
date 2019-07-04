#!/usr/bin/env python3


from starfish import Ocean
from starfish.asset import MemoryAsset
from starfish.agent import MemoryAgent


def main():
    """
    Create a new Ocean instance.
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

    # create a listing specifying the information about the asset
    listing_data = {
        'name': 'The white paper',
        'author': 'Ocean Protocol',
        'license': 'CC0: Public Domain',
        'price': '0'
    }

    # Create a new memory agent to do the work.
    agent = MemoryAgent(ocean)

    # Register the memory asset, with the new account.
    listing = agent.register_asset(asset, listing_data, register_account)

    # Print out the listing did and listing data.
    print('memory listing', listing.listing_id, listing.data)


if __name__ == '__main__':
    main()
