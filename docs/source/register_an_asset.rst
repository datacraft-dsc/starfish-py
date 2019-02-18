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

Loading the asset data and listing
----------------------------------

Next we need to source our asset and it's metadata. An asset is divided into
the following sections:

#. **Asset data** - The actual `file` data residing on secure storage.

#. **Listing** - The `sales` part of the asset. For example a listing will contain price, data samples e.t.c. This can change and you can store multiple listings for a single asset.

#. **Metadata** - The meta data describing the asset. This is the data describing the asset data and contains proof that the asset data has not been changed or altered.


