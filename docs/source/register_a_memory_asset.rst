Register a Memory Asset
=======================

This is the most simplest example, to register an in memory asset.

Creating a new `Ocean` instance
-------------------------------

First import the main starfish ocean library

>>> from starfish import Ocean

Next create an instance and a basic connection to the ocean network

>>> ocean = Ocean()


Create a  Memory Asset
----------------------

For a first test we can try out a basic memory asset to see how the library works.
An asset is a an object containing data that can be sold to another party.

>>> from starfish.asset import MemoryAsset
>>> asset = MemoryAsset(data='Some test data that I want to save for this asset')

Let see what's in the memory asset

>>> print(asset.data)
Some test data that I want to save for this asset
>>> print(asset.did)
None

Setup the Memory Agent
----------------------

We now need an agent to register and manage our memory asset. The agents 
task is to do the actual work of registration.

>>> from starfish.agent import MemoryAgent
>>> agent = MemoryAgent(ocean)

Register the Asset
------------------

Now we can register the asset with the ocean account. This will return
a :class:.Listing object. The listing object will contain all of the information
for selling the asset, such as price, where to obtain the asset, any samples, and more 
information about the asset.

>>> listing = agent.register_asset(asset)
>>> print(listing.asset.did)
did:op:5caa87cc42bf4ef09a96cdc11ba5dccad3659c3618b272c8859d0c8ad4075876360ca948e17e15de6717b61c9d1562dfc3057d8cb8711b9c66702331295bc80e


Example program
---------------

.. literalinclude:: ../../examples/register_memory_asset.py
   :language: python
