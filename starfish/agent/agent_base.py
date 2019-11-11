
"""
    Base agent object
"""

from abc import ABC, abstractmethod
from starfish import Ocean

class AgentBase(ABC):
    """

    Base agent class

    :param ocean: Ocean object that is used by the Agent class
    :type ocean: :class:`.Ocean`
    """
    def __init__(self, ocean):
        """init the the Ocean Object Base with the ocean instance"""

        if not isinstance(ocean, Ocean):
            raise ValueError('You must pass a valid Ocean object')
        self._ocean = ocean

        super().__init__()

    @abstractmethod
    def register_asset(self, asset, listing_data, account):
        """

        Register a squid asset with the ocean network.

        :param asset: the Asset to register, at the moment only a Asset can be used.
        :type asset: :class:`.AssetBase` object to register
        :param dict listing_data: data providing listing information for the asset.
        :param account: Ocean account to use to register this asset.
        :type account: :class:`.Account` object to use for registration.

        :return: A new :class:`.Listing` object that has been registered, if failure then return None.
        :type: :class:`.Listing` class

        For example::

           # get your publisher account
           account = ocean.get_account('0x00bd138abd70e2f00903268f3db08f2d25677c9e')
           agent = SquidAgent(ocean)
           asset = FileAsset(filename='my_file.csv')
           listing_data = {
                'name': 'My data',
                'price': '4',
           }

           listing = agent.register_asset(asset, listing_data, account)

           if listing:
               print(f'registered my listing asset for sale with the did {listing.did}')

        """
        pass

    @abstractmethod
    def validate_asset(self, asset):
        """

        Validate an asset

        :param asset: Asset to validate.
        :return: True if the asset is valid
        """
        pass

    @abstractmethod
    def get_listing(self, listing_id):
        """

        Return an listing from the given listing_id.

        :param str listing_id: Id of the listing.

        :return: a registered listing given a Id of the listing
        :type: :class:`.Listing` class

        """
        pass

    @abstractmethod
    def search_listings(self, text, sort=None, offset=100, page=0):
        """

        Search the off chain storage for an asset with the givien 'text'

        :param str text: Test to search all metadata items for.
        :param sort: sort the results ( defaults: None, no sort).
        :type sort: str or None
        :param int offset: Return the result from with the maximum record count ( defaults: 100 ).
        :param int page: Returns the page number based on the offset.

        :return: a list of assets objects found using the search.
        :type: list of DID strings

        For example::

            # return the 300 -> 399 records in the search for the text 'weather' in the metadata.
            my_result = agent.search_registered_assets('weather', None, 100, 3)

        """
        pass

    @abstractmethod
    def purchase_asset(self, listing, account):
        """

        Purchase an asset using it's listing and an account.

        :param listing: Listing to use for the purchase.
        :type listing: :class:`.Listing`
        :param account: Ocean account to purchase the asset.
        :type account: :class:`.Account` object to use for registration.

        """
        pass

    @abstractmethod
    def is_access_granted_for_asset(self, asset, account, purchase_id=None):
        """

        Check to see if the account and purchase_id have access to the assed data.


        :param asset: Asset to check for access.
        :type asset: :class:`.Asset` object
        :param account: Ocean account to purchase the asset.
        :type account: :class:`.Account` object to use for registration.
        :param str purchase_id: purchase id that was used to purchase the asset.

        :return: True if the asset can be accessed and consumed.
        :type: boolean
        """
        pass

    @abstractmethod
    def get_asset_purchase_ids(self, asset):
        """

        Returns as list of purchase id's that have been used for this asset

        :param asset: Asset to return purchase details.
        :type asset: :class:`.Asset` object

        :return: list of purchase ids
        :type: list

        """
        pass

    @abstractmethod
    def purchase_wait_for_completion(self, asset, account,  purchase_id, timeoutSeconds):
        """

            Wait for completion of the purchase

            TODO: issues here...
            + No method as yet to pass back paramaters and values during the purchase process
            + We assume that the following templates below will always be used.

        """
        pass

    @abstractmethod
    def consume_asset(self, listing, account, purchase_id):
        """
        Consume the asset and download the data. The actual payment to the asset
        provider will be made at this point.

        :param listing: Listing that was used to make the purchase.
        :type listing: :class:`.Listing`
        :param account: Ocean account that was used to purchase the asset.
        :type account: :class:`.Account` object to use for registration.
        :param str purchase_id: purchase id that was used to purchase the asset.

        :return: True if the asset has been consumed and downloaded
        :type: boolean

        """

    @property
    def ocean(self):
        """
        :return: Ocean object
        :type: :class:`.Ocean`
        """
        return self._ocean
