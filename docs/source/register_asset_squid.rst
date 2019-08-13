Register asset using Squid
==========================

This is to show how to register an asset on the Ocean Procotol network using the SquidAgent.

We assume that you have already setup a test `barge` in 'Getting Started'.

Creating a new `Ocean` instance
-------------------------------

First import the main starfish ocean library, and the logging library

>>> from starfish import Ocean

Next create an instance and a basic connection to the ocean network, with
some extra logging so you can see what is happening.

>>> ocean = Ocean(keeper_url='http://localhost:8545')

Loading an account
------------------

Now we need to load an account and see how much ocean tokens and Etherum ether we have.
We will always need some ether to be able to pay for the transaction costs to register and buy an asset
on the Ethereum network.

For our test Ocean network, we will use some ethereum for registering an asset, but
no ocean tokens, since we are not purchasing an asset yet.

>>> account = ocean.get_account('0x00bd138abd70e2f00903268f3db08f2d25677c9e', 'node0')
>>> print(account.ocean_balance, account.ether_balance)
1067 1000000003718520260000000000

Create an Asset
---------------

We now want to create a Starfish asset to register on the block chain.

First we need to create a data asset, using the a URL of an actual asset. In this case
we are going to use an image of a mantaray from the OceanProtocol web site.

>>> from starfish.asset import RemoteDataAsset
>>> asset = DataAsset.create_with_url('MyAsset', 'https://oceanprotocol.com/static/media/mantaray-full.22a18aee.svg')

Let see what's in the data asset

>>> print(asset.metadata)
{'name': 'MyAsset', 'type': 'dataset', 'url': 'https://oceanprotocol.com/static/media/mantaray-full.22a18aee.svg', 'contentType': 'image/svg+xml'}

Now see if the asset has a DID?
>>> print(asset.did)
None

Setup the Squid Agent
---------------------

We now need an agent to register and manage our Asset. The agents
task is to do the actual work of registration. In this example we are going to
use Squid to register this asset.

>>> from starfish.agent import SquidAgent
>>> config = {
    'aquarius_url': 'http://localhost:5000',
    'brizo_url': 'http://localhost:8030',
    'secret_store_url': 'http://localhost:12001',
    'parity_url': 'http://localhost:8545',
    'storage_path': 'squid_py.db',
}
>>> agent = SquidAgent(ocean, config)

Register the Asset
------------------

First we nee to setup some 'Listing data', this is the data that we wish to publish
to anyone who wants to download or buy from us.

>>> listing_data = {'name': 'Mantaray Pic', 'author': 'Ocean Protocol', 'license': 'CC0: Public Domain'}


Now we can register the asset we have created earlier with the ocean account. This will return
a :class:.Listing object. The listing object will contain all of the listing data we supplied.


>>> listing = agent.register_asset(asset, listing_data, account)

We can now view the returned listing. The listing id is the unique identifier that
we can use to load the asset.

>>> print(listing.listing_id)
did:op:00b8348dcfdf4a29b4f973cd0ad43c1d1321c628acf6463597efd21052043e5c

In fact the listing id for squid is the same as the asset id. You can see it is the same by getting the DID of the
asset from the listing.

>>> print(listing.asset.did)
did:op:00b8348dcfdf4a29b4f973cd0ad43c1d1321c628acf6463597efd21052043e5c


Full example to register an Asset on the Ocean Network
------------------------------------------------------
.. literalinclude:: ../../examples/register_asset_squid.py
   :language: python
