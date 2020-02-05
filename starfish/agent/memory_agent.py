"""

Memory Agent class to provide basic functionality for Ocean Agents

"""

import secrets
import re
import json

from ocean_utils.did import id_to_did, did_to_id

from starfish.agent import AgentBase
from starfish.listing import Listing
from starfish.purchase import Purchase
from starfish.utils.did import did_parse


class MemoryAgent(AgentBase):
    """

    Memory Agent class allows to register, list, purchase and consume assets.

    :param ocean: Ocean object that is being used.
    :type ocean: :class:`.Ocean`

    """

    def __init__(self, ocean, *args, **kwargs):
        """init a standard ocean object"""
        AgentBase.__init__(self, ocean)

        if args and isinstance(args[0], dict):
            kwargs = args[0]

        self._memory = {
            'listing_data': {},
            'asset': {},
            'purchase': {}
        }

    def register_asset(self, asset, listing_data, account=None):
        """

        Register a memory asset with the ocean network.

        :param dict metadata: metadata dictionary to store for this asset.
        :param account: Optional, since an account is not assigned to an registered memory asset.
        :type account: :class:`.Account` object to use for registration.

        :return: A new :class:`.Listing` object that has been registered, if failure then return None.
        :type: :class:`.Listing` class

        """

        asset_did = id_to_did(secrets.token_hex(64))
        listing_id = did_to_id(asset_did)
        listing_data['listing_id'] = listing_id,
        listing_data['asset_did'] = asset_did

        self._memory['listing_data'][listing_id] = listing_data
        self._memory['asset'][asset_did] = asset

        listing = None
        if listing_data:
            asset.set_did(asset_did)
            listing = Listing(self, listing_id, asset, listing_data)

        return listing

    def validate_asset(self, asset):
        """

        Validate an asset

        :param asset: Asset to validate.
        :return: True if the asset is valid
        """
        return asset is not None


    def get_listing(self, listing_id):
        """

        Return an listing from the given listing_id.

        :param str listing_id: Id of the listing.

        :return: a registered listing given a Id of the listing
        :type: :class:`.Listing` class

        """
        listing = None
        if listing_id in self._memory['listing_data']:
            listing_data = self._memory['listing_data'][listing_id]
            if listing_data:
                asset_did = listing_data['asset_did']
                asset = self._memory['asset'][asset_did]
                listing = Listing(self, listing_id, asset, listing_data)

        return listing


    def search_listings(self, text, sort=None, offset=100, page=0):
        """

        Search for listings with the givien 'text'

        :param str text: Text to search all listing data for.
        :param sort: sort the results ( defaults: None, no sort).
        :type sort: str or None
        :param int offset: Return the result from with the maximum record count ( defaults: 100 ).
        :param int page: Returns the page number based on the offset.

        :return: a list of listing objects found using the search.
        :type: :class:`.Listing` objects

        For example::

            # return the 300 -> 399 records in the search for the text 'weather' in the metadata.
            my_result = agent.search_registered_assets('weather', None, 100, 3)

        """
        listing_items = None
        for listing_id, listing_data in self._memory['listing_data'].items():
            if re.search(text, json.dumps(listing_data)):
                if listing_items is None:
                    listing_items = {}
                listing_items[listing_id] = listing_data

        return listing_items

    def purchase_asset(self, listing, account):
        """

        Purchase an asset using it's listing and an account.

        :param listing: Listing to use for the purchase.
        :type listing: :class:`.Listing`
        :param account: Ocean account to purchase the asset.
        :type account: :class:`.Account` object to use for registration.

        """
        purchase = None

        purchase_id = secrets.token_hex(64)
        if purchase_id:
            purchase = Purchase(self, listing, purchase_id, account)
            self._memory['purchase'][purchase_id] = (purchase, account.address)

        return purchase

    def purchase_wait_for_completion(self, asset, account,  purchase_id, timeoutSeconds):
        """

            Wait for completion of the purchase

            TODO: issues here...
            + No method as yet to pass back paramaters and values during the purchase process
            + We assume that the following templates below will always be used.

        """
        return True
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

        if purchase_id in self._memory['purchase']:
            purchase, account_address = self._memory['purchase'][purchase_id]
            return purchase and account.is_address_equal(account_address)

        return False

    def get_asset_purchase_ids(self, asset):
        """

        Returns as list of purchase id's that have been used for this asset

        :param asset: DataAsset to return purchase details.
        :type asset: :class:`.DataAsset` object

        :return: list of purchase ids
        :type: list

        """
        return []

    def consume_asset(self, listing, account, purchase_id):
        """
        Consume the asset and download the data. The actual payment to the asset
        provider will be made at this point.

        :param listing: Listing that was used to make the purchase.
        :type listing: :class:`.Listing`
        :param str purchase_id: purchase id that was used to purchase the asset.
        :param account: Ocean account that was used to purchase the asset.
        :type account: :class:`.Account` object to use for registration.

        :return: True if the asset has been consumed and downloaded
        :type: boolean

        """
        return purchase_id in self._memory['purchase']

    @staticmethod
    def is_did_valid(did):
        """
        Checks to see if the DID string is a valid DID for this type of Asset.
        This method only checks the syntax of the DID, it does not resolve the DID
        to see if it is assigned to a valid Asset.

        :param str did: DID string to check to see if it is in a valid format.

        :return: True if the DID is in the format 'did:dep:xxxxx'
        :type: boolean
        """
        data = did_parse(did)
        return not data['path']
