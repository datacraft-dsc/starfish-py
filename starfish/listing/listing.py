
"""
   Listing class
"""

from starfish.account import AccountObject

class Listing():
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
    def __init__(self, agent, did, asset, data):
        """init the the Listing Object Base with the agent instance"""
        self._agent = agent
        self._did = did
        self._asset = asset
        self._data = data


    def purchase(self, account):
        """

        Purchase the underlying asset within this listing using the account details, return a purchased asset
        with the service_agreement_id ( purchase_id ) set.

        :param account: account to use to purchase this asset.
        :type account: :class:`.Account`

        :return: SquidPurchase object that has information about this listing, asset and purcase id.
        :type: :class:`.SquidPurchase`

        """
        if not isinstance(account, AccountObject):
            raise TypeError('You need to pass an Account object')

        if not account.is_valid:
            raise ValueError('You must pass a valid account')

        return self._agent.purchase_asset(self, account)

    @property
    def agent(self):
        """

        :return: Agent object that created this listing
        :type: :class:`.SquidAgent`
        """
        return self._agent

    @property
    def did(self):
        """
        :return: did of the listing
        :type: string
        """
        return self._did

    @property
    def data(self):
        """

        :return: data of the listing
        :type: dict or None
        """
        return self._data

    @property
    def asset(self):
        """

        :return: asset held by the listing
        :type: :class:`.Asset`
        """
        return self._asset

    @property
    def is_empty(self):
        """

        Checks to see if this Listinng is empty.

        :return: True if this listing is empty else False.
        :type: boolean
        """
        return self._did is None or self._did is None or self._asset is None
