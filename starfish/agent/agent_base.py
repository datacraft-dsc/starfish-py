
"""
    Base agent object
"""

from abc import (
    ABC,
    abstractmethod
)

from typing import Any

from starfish.ddo.ddo import DDO
from starfish.types import (
    ListingData,
    TAsset,
    TListing
)


class AgentBase(ABC):
    """

    Base agent class

    :param ddo: DDO of the Agent
    """
    def __init__(self, ddo: DDO = None) -> None:
        """init the the Agent Base class"""

        self._ddo = ddo

        super().__init__()

    @abstractmethod
    def register_asset(self, asset: TAsset) -> TAsset:
        """

        Register an asset with an Agent

        :param asset: asset object to register
        :type asset: :class:`.DataAsset` object to register

        :return: A :class:`.AssetBase` object that has been registered, if failure then return None.
        :type: :class:`.AssetBase` class

        """
        pass

    @abstractmethod
    def create_listing(self, listing_data: ListingData, asset_did: str) -> TListing:
        """

        Create a listing on the market place for this asset

        :param dict listing_data:  Listing inforamiton to give for this asset
        :param str asset_did: asset DID to assign to this listing
        :return: A new :class:`.Listing` object that has been registered, if failure then return None.
        :type: :class:`.Listing` class

        """
        pass

    @abstractmethod
    def update_listing(self, listing: TListing) -> None:
        """

        Update the listing to the agent server.

        :param listing: Listing object to update
        :type listing: :class:`.Listing` class

        """
        pass

    @abstractmethod
    def validate_asset(self, asset: TAsset) -> bool:
        """

        Validate an asset

        :param asset: Asset to validate.
        :return: True if the asset is valid
        """
        pass

    @abstractmethod
    def get_listing(self, listing_id: str) -> TListing:
        """

        Return an listing from the given listing_id.

        :param str listing_id: Id of the listing.

        :return: a registered listing given a Id of the listing
        :type: :class:`.Listing` class

        """
        pass

    @abstractmethod
    def search_listings(self, text: str, sort: Any = None, offset: int = 100, page: int = 0) -> Any:
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
    def purchase_asset(self, listing: Any, account: Any) -> Any:
        """

        Purchase an asset using it's listing and an account.

        :param listing: Listing to use for the purchase.
        :type listing: :class:`.Listing`
        :param account: Account to purchase the asset.
        :type account: :class:`.Account` object to use for registration.

        """
        pass

    @abstractmethod
    def is_access_granted_for_asset(self, asset_did: str, account: Any, purchase_id: str = None) -> bool:
        """

        Check to see if the account and purchase_id have access to the assed data.


        :param str asset_did: Asset DID to check for access.
        :param account: Account to purchase the asset.
        :type account: :class:`.Account` object to use for registration.
        :param str purchase_id: purchase id that was used to purchase the asset.

        :return: True if the asset can be accessed and consumed.
        :type: boolean
        """
        pass

    @abstractmethod
    def get_asset_purchase_ids(self, asset: Any) -> Any:
        """

        Returns as list of purchase id's that have been used for this asset

        :param asset: Asset to return purchase details.
        :type asset: :class:`.Asset` object

        :return: list of purchase ids
        :type: list

        """
        pass

    @abstractmethod
    def purchase_wait_for_completion(self, asset_did: str, account: Any,  purchase_id: str, timeoutSeconds: int) -> None:
        """

            Wait for completion of the purchase

            TODO: issues here...
            + No method as yet to pass back paramaters and values during the purchase process
            + We assume that the following templates below will always be used.

        """
        pass

    @abstractmethod
    def consume_asset(self, listing: Any, account: Any, purchase_id: str) -> bool:
        """
        Consume the asset and download the data. The actual payment to the asset
        provider will be made at this point.

        :param listing: Listing that was used to make the purchase.
        :type listing: :class:`.Listing`
        :param account: Account that was used to purchase the asset.
        :type account: :class:`.Account` object to use for registration.
        :param str purchase_id: purchase id that was used to purchase the asset.

        :return: True if the asset has been consumed and downloaded
        :type: boolean

        """

    @property
    def did(self) -> str:
        if self._ddo:
            return self._ddo.did

    @property
    def ddo(self) -> DDO:
        """

        Return the did for this remote agent.

        :return: did of the registered agent
        :type: string
        """
        return self._ddo
