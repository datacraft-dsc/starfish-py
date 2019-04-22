
"""
    Basic Purchase class
"""

from starfish.account import Account
from starfish.purchase.purchase_base import PurchaseBase

class Purchase(PurchaseBase):
    """

    This class is returned by purchasing an asset uning the :func:`.Listing.purchase` method.

    :param agent: agent that was used create this object.
    :type agent: :class:`.Agent`
    :param listing: Listing used to purchase this asset.
    :type listing: :class:`.Listing`
    :param purchase_id: purchase_id used to buy this asset.
    :type purchase_id: str

    """

    def __init__(self, agent, listing, purchase_id):
        """init the the Purchase Object Base with the agent instance"""
        super().__init__(agent,listing,purchase_id)

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

        return self._agent.is_access_granted_for_asset(self._listing.asset, self._purchase_id, account)

    def is_completed(self, account):
        """

        Currently the same as `is_purchase_valid`, but renamed to be more meaningfull
        with the `wait_for_completion` method.

        :param account: account that made the purchase
        :type account: :class: `.Account`

        :return: boolean True if the purchase has completed and finished, else
        False if the purchase is invalid or the has not finished.

        """
        return self.is_purchase_valid(account)

    def wait_for_completion(self, timeoutSeconds=60):
        """

        Some purchases ( squid ), require to wait for the smart contracts to complete
        This method will call the underlying agent to wait for the purchase to complete

        :param integer timeoutSeconds: Optional seconds to waif to purchase to complete. Default: 60 seconds
        :return: True if successfull or an error message if failed
        :type: string or boolean

        :raises OceanPurchaseError: if the correct events are not received

        """
        if not self.is_purchased:
            raise StarfishPurchaseError('You need to purchase this asset before waiting')

        return self._agent.purchase_wait_for_completion(self._purchase_id, timeoutSeconds)


    def consume(self, account, download_path):
        """

        Consume a purchased asset. This call will try to download the asset data.

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

        return self._agent.consume_asset(self._listing, self._purchase_id, account, download_path)

    @property
    def get_type(self):
        return "asset"

    @property
    def is_purchased(self):
        """
        :return: True if this asset is a purchased asset.
        :type: boolean
        """
        return not self._purchase_id is None
