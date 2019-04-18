
"""
   Listing Base class
"""

from abc import ABC, abstractmethod

class ListingBase(ABC):
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
    def __init__(self, agent, did, asset, data, listing_id=None):
        """init the the Listing Object Base with the agent instance"""
        self._agent = agent
        self._did = did
        self._asset = asset
        self._data = data
        self._listing_id=listing_id
        super().__init__()

    @abstractmethod
    def purchase(self, account):
        """

        Purchase the underlying asset within this listing using the account details, return a purchased asset
        with the service_agreement_id ( purchase_id ) set.

        :param account: account to use to purchase this asset.
        :type account: :class:`.Account`

        :return: SquidPurchase object that has information about this listing, asset and purcase id.
        :type: :class:`.SquidPurchase`

        """
        pass

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
    def listing_id(self):
        """

        :return: the listing id
        :type: str or None
        """
        return self._listing_id

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
