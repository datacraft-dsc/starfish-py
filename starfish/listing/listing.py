
"""
   Listing class
"""

from starfish.listing.listing_base import ListingBase
from starfish.account import Account

class Listing(ListingBase):
    """
        Create a Listing object

        :param agent: agent object that created the listing.
        :type agent: :class:`.Agent` object to assign to this Listing
        :param str did: did of the listing, this can be the did of the underling asset.
        :param asset: the core asset for this listing
        :type asset: :class:`.Asset` object
        :param data: data of the listing
        :type data: dict
    """


    def purchase(self, account):
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
