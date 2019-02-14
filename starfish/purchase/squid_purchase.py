
"""

SquidPurchase class to hold Squid purchased asset information.

"""

from eth_utils import remove_0x_prefix

from squid_py.did import did_to_id

from starfish import Account
from starfish.models.squid_model import SquidModel
from starfish.utils.did import did_parse
from starfish.purchase.purchase_object import PurchaseObject


# from starfish import logger


class SquidPurchase(PurchaseObject):
    """

    :param agent: ocean object to use to connect to the ocean network.
    :type agent: OceanObject
    :param purchase_id: purchase_id used to buy this asset.
    :type purchase_id: str
    :param listing: Listing used to purchase this asset
    :type listing: :class:`.Listing`

    """
    def __init__(self, agent, listing, purchase_id):
        """init a standard ocean object"""
        PurchaseObject.__init__(self, agent, listing)
        self._purchase_id = purchase_id

    def is_purchase_valid(self, account):
        """

        Test to see if this purchased asset can be accessed and is valid.

        :param account: account to used to check to see if this asset is purchased and has access using this account.
        :type account: :class:`.Account`

        :return: boolean value if this asset has been purchased
        :type: boolean
        """
        if not self.is_purchased:
            return False

        if not isinstance(account, Account):
            raise TypeError('You need to pass an Account object')

        if not account.is_valid:
            raise ValueError('You must pass a valid account')


        model = self.agent.squid_model        
        return model.is_access_granted_for_asset(self._listing, self._purchase_id, account)

    def consume(self, account, download_path):
        """

        Consume a purchased asset. This call will try to download the asset data
        that you have already called using the :func:`listing.purchase` method.

        You can call the :func:`is_purchased` property before hand to check that you
        have already purchased this asset.

        :param account: account to used to consume this asset.
        :type account: :class:`.Account`
        :param str download_path: Path to download the asset files too.

        :return: data returned from the asset , or False
        :type: object or False

        """
        if not self.is_purchased:
            return False

        if not isinstance(account, Account):
            raise TypeError('You need to pass an Account object')

        if not account.is_valid:
            raise ValueError('You must pass a valid account')

        model = self.agent.squid_model
        return model.consume_asset(self._listing, self._purchase_id, account, download_path)

    @property
    def is_purchased(self):
        """
        :return: True if this asset is a purchased asset.
        :type: boolean
        """
        return not self._purchase_id is None

    @property
    def purchase_id(self):
        """
        :return: The purchase id for this asset, if not purchased then return None.
        :type: str
        """
        return self._purchase_id

