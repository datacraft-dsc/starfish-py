#!/usr/bin/env python3

import json

from starfish import Ocean
from starfish.asset import MemoryAsset
from starfish.agent import SurferAgent


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
    # account = ocean.get_account('0x00bd138abd70e2f00903268f3db08f2d25677c9e')

    # Print out the account's ocean balance.
    # print('my account ocean balance:', account.ocean_balance)
    # print('my account ether balance:', account.ether_balance)

    # Now create a memory asset
    asset = MemoryAsset(data='Some test data that I want to save for this asset')

    # NOTE: In surfer
    # MemoryAsset extends ADataAsset
    #   ADataAsset extends AAsset implements DataAsset
    #     AAsset implements Asset
    #       sets this.id=Hex.toString(Hash.keccak256(meta));
    # In Python there's only the DID, not the id

    # Print the memory asset out
    print('my asset:', asset.data)

    # Print the memory asset metadata out
    print('my asset metadata:')
    metadata_json = json.dumps(asset.metadata, sort_keys=True, indent=2)
    print(metadata_json)

    # Create a new memory agent to do the work.
    agent = SurferAgent(ocean)

    # Register the memory asset.
    # NOTE: In surfer the agent is a RemoteAgent and
    # public class RemoteAgent extends AAgent implements Invokable {
    #    public RemoteAsset registerAsset(Asset a) {
    # Whereas in python we return a listing
    ra = agent.register_asset(asset)

    # Print out the remote asset
    print('surfer remote asset', ra)

if __name__ == '__main__':
    main()
