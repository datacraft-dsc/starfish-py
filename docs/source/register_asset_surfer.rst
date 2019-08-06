Register asset on Surfer
========================

This is to show how to register an asset on Surfer.

Surfer is a centralized server that allows the server url to be registered on the Ocean Network.

Any asset registered with Surfer will not be written to the block chain.

We assume that you have already setup a test `barge` in 'Getting Started'.

Creating a new `Ocean` instance
-------------------------------

First import the main starfish ocean library, and the logging library

>>> from starfish import Ocean
>>> import logging

Next create an instance and a basic connection to the ocean network, with
some extra logging so you can see what is happening.

>>> ocean = Ocean(keeper_url='http://localhost:8545')

Create an Asset
---------------

We now want to create an Ocean asset to register with Surfer, we can store it's metadata and data
all with Surfer.

First we need to create a data asset, using some test data.

>>> from starfish.asset import DataAsset
>>> asset = DataAsset.create('MyAsset', 'Here is some test text that I want to save in Surfer service')

Let see what's in the data asset

>>> print(asset.metadata)
{'name': 'MyAsset', 'type': 'dataset', 'contentType': 'text/plain; charset=utf-8'}

Now see if the asset has a DID?

>>> print(asset.did)
None

Setup the Surfer Agent
----------------------

We now need an agent to register and manage our Asset. The agents
task is to do the actual work of registration.

>>> from starfish.agent import SurferAgent
>>> agent = SquidAgent(ocean, SURFER_AGENT_PARAMETERS)

Register the Asset
------------------

First we need to create some listing data. This data is linked with the asset for public
view and provide more information about the asset.

>>> listing_data = {'name': 'My data', 'author': 'Help writer', 'license': 'CC0: Public Domain'}

Now we can register the asset we have created earlier. This will return
a :class:.Listing object. The listing object will contain all of the information
for selling the asset, such as price, where to obtain the asset, any samples, and more
information about the asset.

>>> listing = agent.register_asset(asset, listing_data)
>>> print(listing.asset.did)
did:op:5caa87cc42bf4ef09a96cdc11ba5dccad3659c3618b272c8859d0c8ad4075876360ca948e17e15de6717b61c9d1562dfc3057d8cb8711b9c66702331295bc80e

You will notice that the asset url returned contains two id's. The first is the regisered DID on the
Ocean Protocol block chain, the second id is the internall asset id registered on the Surfer.

Saving the Asset
----------------
With Surfer we can now save the asset data. To do this we just need to call the `upload` method in the Surfer Agent.

>>> agent.upload_asset(asset)

N.B. Rememeber you can only upload and download in asset with Surfer if you have regisetred it before hand.


Full example to register and upload an Asset on Surfer
------------------------------------------------------
.. literalinclude:: ../../examples/register_upload_asset_surfer.py
   :language: python
