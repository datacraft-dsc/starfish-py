Register an Asset
=================

Creating a new `Ocean` instance
-------------------------------

First import the main starfish ocean library

>>> from starfish import Ocean

Next create an instance and a basic connection to the ocean network

>>> ocean = Ocean(contracts_path='artifacts', keeper_url='http://localhost:8545')

Loading an account
------------------

Now we need to load an account and see how much ocean tokens and ether we have

>>> account = ocean.get_account('0x00bd138abd70e2f00903268f3db08f2d25677c9e')
>>> print(account.ocean_balance, account.ether_balance)
1067 1000000003718520260000000000

Create a  Memory Asset
----------------------

For a first test we can try out a basic memory asset to see how the library works

>>> from starfish.asset import MemoryAsset
>>> asset = MemoryAsset(data='Some test data that I want to save for this asset')

Let see what's in the memory asset

>>> print(asset.data)
Some test data that I want to save for this asset
>>> print(asset.did)
None

Setup the Memory Agent
----------------------

We now need an agent to register and manage our memory asset.

>>> from starfish.agent import MemoryAgent
>>> agent = MemoryAgent(ocean)

Register the Asset
------------------

Now we can register the asset with the ocean account

>>> listing = agent.register_asset(asset, account)
>>> print(listing.asset.did)
did:op:5caa87cc42bf4ef09a96cdc11ba5dccad3659c3618b272c8859d0c8ad4075876360ca948e17e15de6717b61c9d1562dfc3057d8cb8711b9c66702331295bc80e



