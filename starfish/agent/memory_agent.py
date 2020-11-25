"""

Memory Agent class to provide basic functionality for Ocean Agents

"""

import json
import re
import secrets
from typing import Any

from starfish.agent.agent_base import AgentBase
from starfish.listing import Listing
from starfish.network.ddo import DDO
from starfish.network.did import (
    decode_to_asset_id,
    did_generate_random
)
from starfish.purchase import Purchase
from starfish.types import (
    ListingData,
    TAsset,
    TListing
)
from starfish.utils.crypto_hash import hash_sha3_256


class MemoryAgent(AgentBase):
    """

    Memory Agent class allows to register, list, purchase and consume assets.

    :param ddo: ddo to access the agent
    :type ddo: :class:`.DDO`

    """

    def __init__(self, ddo: DDO = None) -> None:

        if ddo is None:
            did = did_generate_random()
            ddo = DDO(did)

        AgentBase.__init__(self, ddo=ddo)

        self._memory = {
            'listing': {},
            'asset': {},
            'purchase': {}
        }

    def register_asset(self, asset: TAsset) -> TAsset:
        """

        Register a memory asset.

        :param object metadata: asset object to register for this asset.

        :return: A :class:`.AssetBase` object that has been registered, if failure then return None.
        :type: :class:`.AssetBase` class

        """

        asset_id = hash_sha3_256(asset.metadata_text)
        did = f'{self._ddo.did}/{asset_id}'

        self._memory['asset'][did] = asset
        asset.set_did(did)
        return asset

    def create_listing(self, listing_data: ListingData, asset_did: str) -> TListing:
        """

        Create a listing on the market place for this asset

        :param dict listing_data:  Listing inforamiton to give for this asset
        :param str asset_did: asset DID to assign to this listing
        :return: A new :class:`.Listing` object that has been registered, if failure then return None.
        :type: :class:`.Listing` class

        """
        listing = None
        if listing_data:
            listing_id = decode_to_asset_id(asset_did)
            listing_data['listing_id'] = listing_id,
            listing_data['asset_did'] = asset_did
            listing = Listing(self, listing_id, asset_did, listing_data)
            self._memory['listing'][listing_id] = listing
        return listing

    def update_listing(self, listing: TListing) -> None:
        """

        Update the listing to the agent server.

        :param listing: Listing object to update
        :type listing: :class:`.Listing` class

        """
        self._memory['listing'][listing.listing_id] = listing

    def validate_asset(self, asset: TAsset) -> bool:
        """

        Validate an asset

        :param asset: Asset to validate.
        :return: True if the asset is valid
        """
        return asset is not None

    def get_listing(self, listing_id: str) -> TListing:
        """

        Return an listing from the given listing_id.

        :param str listing_id: Id of the listing.

        :return: a registered listing given a Id of the listing
        :type: :class:`.Listing` class

        """
        listing = None
        if listing_id in self._memory['listing']:
            listing = self._memory['listing'][listing_id]
        return listing

    def search_listings(self, text: str, sort: str = None, offset: int = 100, page: int = 0) -> Any:
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
        listing_id_list = []
        for listing_id, listing in self._memory['listing'].items():
            if re.search(text, json.dumps(listing.data)):
                listing_id_list.append(listing.listing_id)

        return listing_id_list

    def purchase_asset(self, listing: Any, account: Any) -> Any:
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

    def purchase_wait_for_completion(self, asset: Any, account: Any,  purchase_id: str, timeoutSeconds: int) -> bool:
        """

            Wait for completion of the purchase

            TODO: issues here...
            + No method as yet to pass back paramaters and values during the purchase process
            + We assume that the following templates below will always be used.

        """
        return True

    def is_access_granted_for_asset(self, asset: Any, account: Any, purchase_id: str = None) -> bool:
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

    def get_asset_purchase_ids(self, asset: Any) -> Any:
        """

        Returns as list of purchase id's that have been used for this asset

        :param asset: DataAsset to return purchase details.
        :type asset: :class:`.DataAsset` object

        :return: list of purchase ids
        :type: list

        """
        return []

    def consume_asset(self, listing: Any, account: Any, purchase_id: str) -> bool:
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
