"""


   Listing class


"""

from starfish.account import Account

from starfish.listing.listing_base import ListingBase


class Listing(ListingBase):
    """
        Create a Listing object

        :param agent: agent object that created the listing.
        :type agent: :class:`.Agent` object to assign to this Listing
        :param str did: did of the listing, this can be the did of the underling asset.
        :param str asset_did: the core asset DID for this listing
        :param data: data of the listing
        :param ddo: Optional ddo for the listing
        :type data: dict
    """

    def purchase(self, account: Account) -> bool:
        """

        Purchase the underlying asset within this listing using the account details, return a purchased asset
        with the service_agreement_id ( purchase_id ) set.

        :param account: account to use to purchase this asset.
        :type account: :class:`.Account`

        :return: SquidPurchase object that has information about this listing, asset and purcase id.
        :type: :class:`.SquidPurchase`

        """
        if not isinstance(account, Account):
            raise TypeError('You need to pass an Account object')

        return self._agent.purchase_asset(self, account)

    def is_purchased(self, account: Account) -> bool:
        """

        Return true if the account has already purchased this listing/asset

        :param account: account to test for this purchase of this asset.
        :type account: :class:`.Account`

        :return: result if has purchased this asset
        :type: boolean

        """
        if not isinstance(account, Account):
            raise TypeError('You need to pass an Account object')

        return self._agent.is_access_granted_for_asset(self.asset_did, account)

    def set_published(self, value: bool) -> None:
        """

        Set the published value

        :params boolean value: Published value True or False

        """
        if self._data and isinstance(self._data, dict) and 'status' in self._data:
            if value:
                self._data['status'] = 'published'
            else:
                self._data['status'] = 'unpublished'

    @property
    def is_published(self) -> bool:
        """

        Return a True if this listing is published

        :return: True of False if this listing is published
        :type: boolean

        """
        if self._data and isinstance(self._data, dict) and 'status' in self._data:
            return self._data['status'] == 'published'
        return False

    @property
    def get_purchase_ids(self) -> str:
        return self._agent.get_asset_purchase_ids(self.asset_did)

    def __str__(self) -> str:
        s = 'Listing: agent=' + self._agent.__class__.__name__ + ', '
        s += 'listing_id=' + self._listing_id + ', '
        s += 'asset_did=' + self._asset_did + ', '
        s += 'data=' + str(self._data)
        return s
