
"""
    Operation class
"""

import logging
from starfish.account import Account
from starfish.purchase.purchase_base import PurchaseBase
logger = logging.getLogger('starfish.squid_operation')

class SquidOperation(PurchaseBase):
    """

    This class is returned by purchasing an invokable asset uning the :func:`.Listing.purchase` method.

    :param agent: agent that was used create this object.
    :type agent: :class:`.Agent`
    :param listing: Listing used to purchase this asset.
    :type listing: :class:`.Listing`
    :param purchase_id: purchase_id used to buy this asset.
    :type purchase_id: str

    """

    def __init__(self, agent, listing, purchase_id):
        """init the the Operation Object Base with the agent instance"""
        super().__init__(agent, listing, purchase_id)

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

    def invoke(self, account, payload):
        """

        Call invoke

        You can call the :func:`is_purchased` property before hand to check that you
        have already purchased this asset.

        :param account: account to used to consume this asset.
        :type account: :class:`.Account`
        :param str payload: Json payload that the invoke operation needs.

        :return: data returned from the asset , or False
        :type: object or False

        """
        if not self.is_purchased:
            return False

        if not isinstance(account, Account):
            raise TypeError('You need to pass an Account object')

        if not account.is_valid:
            raise ValueError('You must pass a valid account')
        logger.info(f'calling invoke in operation.py with payload: {payload}')
        return self._agent.invoke_operation(self._listing, self._purchase_id, account,
                                            payload)

    @property
    def get_type(self):
        return "operation"

    @property
    def is_purchased(self):
        """
        :return: True if this asset is a purchased asset.
        :type: boolean
        """
        return not self._purchase_id is None
