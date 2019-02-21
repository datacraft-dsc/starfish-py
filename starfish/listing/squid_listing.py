
"""

Squid Listing class to hold Ocean listing information such as an asset id and metadata

"""

from eth_utils import remove_0x_prefix

from squid_py.did import did_to_id

from starfish import Account
from starfish.listing import ListingObject

# from starfish import logger

class SquidListing(ListingObject):
    """

    The listing object is created by the :class:`.SquidAgent` class.

    :param agent: agent object that created this listing.
    :type agent: :class:`.SquidAgent`
    :param asset: Asset object to set with this listing.
    :type asset: :class:`.Asset` object
    :param any data: listing data to provide information about this listing
    :type data: dict

    """
    def __init__(self, agent, asset, data):
        """

        init a standard ocean object.
        For squid we have metadata but it is in a DDO,
        so the creator of this class sends the metadata as a DDO.

        """
        ListingObject.__init__(self, agent, asset, data)


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

        if not account.is_valid:
            raise ValueError('You must pass a valid account')

        return self._agent.purchase_asset(self, account)
