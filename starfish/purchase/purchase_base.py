
"""
    Base Purchase class
"""
from abc import ABC, abstractmethod


class PurchaseBase(ABC):

    def __init__(self, agent, listing, purchase_id):
        """init the the Purchase Object Base with the agent instance"""
        self._agent = agent
        self._listing = listing
        self._purchase_id = purchase_id
        super().__init__()

    @abstractmethod
    def is_purchase_valid(self, account):
        """

        """
        pass

    @property
    def agent(self):
        """
        :return: Agent object
        :type: :class:`.AgentObject`
        """
        return self._agent

    @property
    def listing(self):
        """
        :return: Listing object
        :type: :class:`.ListingObject'`
        """
        return self._listing

    @property
    def purchase_id(self):
        """
        :return: purchase id
        :type: str
        """
        return self._purchase_id

    @property
    @abstractmethod
    def is_purchased(self):
        """
        :return: True if this asset is a purchased asset.
        :type: boolean
        """
        pass
