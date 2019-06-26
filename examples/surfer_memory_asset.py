#!/usr/bin/env python3

import json
import logging

from starfish import Ocean
from starfish.asset import MemoryAsset
from starfish.agent import SurferAgent

def main():
    """
    Create a new Ocean instance.
    You can pass 'log_level=logging.DEBUG' parameter to get full debug
    logging information.
    """
    ocean = Ocean(log_level=logging.DEBUG)

    # Now create a memory asset
    asset = MemoryAsset(data='Some test data that I want to save for this asset')

    # NOTE: In starfish-java
    # MemoryAsset extends ADataAsset
    #   ADataAsset extends AAsset implements DataAsset
    #     AAsset implements Asset
    #       sets this.id=Hex.toString(Hash.keccak256(meta));
    # In Python there's only the DID, not the id

    # Print the memory asset out
    print('my asset:', asset.data)

    # Create a new memory agent to do the work.
    surfer_url = 'http://52.187.164.74:8080'
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

    # Register the memory asset.
    # NOTE: In surfer the agent is a RemoteAgent and
    # public class RemoteAgent extends AAgent implements Invokable {
    #    public RemoteAsset registerAsset(Asset a) {
    # Whereas in python we return a listing
    ra = agent.register_asset(asset, listing_data)

    # Print out the remote asset
    print('surfer remote asset', ra)

if __name__ == '__main__':
    main()
