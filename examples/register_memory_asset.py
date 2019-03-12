#!/usr/bin/env python3

import logging

from starfish import Ocean
from starfish.asset import MemoryAsset
from starfish.agent import MemoryAgent


def main():
    """
    Create a new Ocean instance.
    You can pass 'log_level=logging.DEBUG' parameter to get full debug 
    logging information.
    """
    ocean = Ocean(contracts_path='artifacts', keeper_url='http://localhost:8545')

    """
    Get our first account - in test the account numbers are published
    at https://docs.oceanprotocol.com/concepts/testnets/
    """
    account = ocean.get_account('0x00bd138abd70e2f00903268f3db08f2d25677c9e')

    """
    Print out the account's ocean balance.
    """
    print('my account', account.ocean_balance)

    """
    Now create a memory asset
    """
    asset = MemoryAsset(data='Some test data that I want to save for this asset')

    """
    Print the memory asset out
    """
    print('my asset', asset)

    """
    Create a new memory agent to do the work.
    """
    agent = MemoryAgent(ocean)

    """
    Register the memory asset.
    """
    listing = agent.register_asset(asset, account)

    """
    Print out the listing did and listing data.
    """
    print('memory listing', listing.did, listing.data)

if __name__ == '__main__':
    main()
