
"""

Squid Listing class to hold Ocean listing information such as an asset id and metadata

"""

from eth_utils import remove_0x_prefix

from squid_py.did import did_to_id

from starfish import Account
from starfish.utils.did import did_parse
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

    @staticmethod
    def is_did_valid(did):
        """
        Checks to see if the DID string is a valid DID for this type of Asset.
        This method only checks the syntax of the DID, it does not resolve the DID
        to see if it is assigned to a valid Asset.

        :param str did: DID string to check to see if it is in a valid format.

        :return: True if the DID is in the format 'did:op:xxxxx'
        :type: boolean
        """
        data = did_parse(did)
        return not data['path']
