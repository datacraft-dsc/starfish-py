Register asset on a remote agent
================================

This is to show how to register an asset on a remote agent.

The remote agent (Surfer) is a centralized server that allows the server url to be registered on the Ocean Network.

Any asset registered with a remote agent will not be written to the block chain, but the returned
DID will contain the Remote Agent DID/asset_id. This can be resolved by using the Ocean Protocol network
to obtain the asset.

We assume that you have already setup a test `barge` in 'Getting Started', with a running remote agent in Barge.

Creating a new `Ocean` instance
-------------------------------

First import the main starfish ocean library, and the logging library

>>> from starfish import Ocean

Next create an instance and a basic connection to the ocean network, with
some extra logging so you can see what is happening.

>>> ocean = Ocean(keeper_url='http://localhost:8545')

Create an Asset
---------------

We now want to create an Ocean asset to register with the remote agent, we can store it's metadata and data
all with agent.

First we need to create a data asset, using some test data.

>>> from starfish.asset import DataAsset
>>> asset = DataAsset.create('MyAsset', 'Here is some test text that I want to save in remote agent service')

Let see what's in the DataAsset metadata

>>> print(asset.metadata)
{'name': 'MyAsset', 'type': 'dataset', 'contentType': 'text/plain; charset=utf-8'}

and what is in the DataAsset data property

>>> print(asset.data)
Here is some test text that I want to save in remote agent service


Now see if the asset has a DID?

>>> print(asset.did)
None

Setup the Remote Agent
----------------------

We now need an agent to register and manage our Asset. The agents
task is to do the actual work of registration.

First we need to import the agent and setup it's configuration for the local test Barge.

>>> from starfish.agent import RemoteAgent
>>> url = 'http://localhost:8080'
>>> options = {
        'url': url,
        'username': 'test',
        'password':  'foobar',
    }

Since this is probably the first time we are using remote agent, we need to register
all of the services that remote agent supports on the Ocean Network. In our case
the Ocean Network is going to be the local Barge.

So first create a DDO record for the local remote agent service.

>>> ddo = RemoteAgent.generate_ddo(url)

Lets see what the DID of the remote agent service is going to be?

>>> print(ddo.did)
did:dep:45fd1d44764047808b313bf777d98d6304fdf9ff3ba7463aa4346e888ff5041c

We can now create the remote agent using teh options provided

>>> agent = RemoteAgent(ocean, did=ddo.did, ddo=ddo, options=options)

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

We can find out what the listing id has been assigned to us by remote agent

>>> print(listing.listing_id)
a3392ea6f7b7301bb81c4fe58ad0959360d53662ce3a3d35589f9fbd0e276699

Lets find out what the asset or listing DID

>>> print(listing.did)
did:dep:45fd1d44764047808b313bf777d98d6304fdf9ff3ba7463aa4346e888ff5041c/3bd774d7d7ee5239c26b39b44b659a2488cc3fcdd17140274b04bfc0a05520f5

You will notice that the listing DID returned contains two id's. The first is the regisered DID on the
Ocean Protocol block chain, the second id is the internall asset id registered on the remote agent.

To check that the asset id is the same we can print out the asset id

>>> print(listing.asset.asset_id)
0x3bd774d7d7ee5239c26b39b44b659a2488cc3fcdd17140274b04bfc0a05520f5

Saving the Asset
----------------
With the remote agent we can now save the asset data. To do this we just need to call the `upload` method in the remote agent.

>>> agent.upload_asset(asset)
True


N.B. Rememeber you can only upload and download in asset with the remote agent if you have registered it before hand.


Full example to register and upload an Asset on Remote Agent
------------------------------------------------------------
.. literalinclude:: ../../examples/register_upload_asset_remote_agent.py
   :language: python
