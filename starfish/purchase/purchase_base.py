
"""
    Base Purchase class
"""
from abc import (
    ABC,
    abstractmethod
)


class PurchaseBase(ABC):

    def __init__(self, agent, listing, purchase_id, account):
        """init the the Purchase Object Base with the agent instance"""
        self._agent = agent
        self._listing = listing
        self._purchase_id = purchase_id
        self._account = account
        super().__init__()

    @property
    def agent(self):
        """
        :return: Agent object
        :type: :class:`.Agent`
        """
        return self._agent

    @property
    def listing(self):
        """
        :return: Listing object
        :type: :class:`.Listing'`
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
    def account(self):
        """
        :return: account that is doing the purchase
        :type: :class:`.Account`
        """
        return self._account

    @property
    @abstractmethod
    def is_purchased(self):
        """
        :return: True if this asset is a purchased asset.
        :type: boolean
        """
        pass

    @property
    @abstractmethod
    def is_purchase_valid(self):
        """
        :return: True if this asset is a valid purchase.
        :type: boolean
        """
        pass
