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
    print('my account ocean balance:', account.ocean_balance)
    print('my account ether balance:', account.ether_balance)

    """
    Now create a memory asset
    """
    asset = MemoryAsset(data='Some test data that I want to save for this asset')

    """
    Print the memory asset out
    """
    print('my asset:', asset.data)

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

"""

./example/register_memory_asset.py

Example output:

    Using default logging settings.
    my account ocean balance: 181
    my account ether balance: 1000000001878471200000000000
    my asset: Some test data that I want to save for this asset
    memory listing did:op:9e51b6167180f675586bda86148bc6300cb06da954c7c05d55a55ce0ea9c1b8e54fd280cbefcd5b58410b0b651e8728efc021b94bdd281e8bca4fbac2195544a {'did': 'did:op:9e51b6167180f675586bda86148bc6300cb06da954c7c05d55a55ce0ea9c1b8e54fd280cbefcd5b58410b0b651e8728efc021b94bdd281e8bca4fbac2195544a', 'asset_did': 'did:op:9e51b6167180f675586bda86148bc6300cb06da954c7c05d55a55ce0ea9c1b8e54fd280cbefcd5b58410b0b651e8728efc021b94bdd281e8bca4fbac2195544a'}

"""
