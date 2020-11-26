
"""
   Listing Base class
"""

from abc import (
    ABC,
    abstractmethod
)
from typing import (
    Any,
    Generic
)
from starfish.agent.agent_base import AgentBase
from starfish.network.account_base import AccountBase
from starfish.network.ddo import DDO
from starfish.types import TListingBase


class ListingBase(ABC, Generic[TListingBase]):
    """
        Create a Listing object

        :param agent: agent object that created the listing.
        :type agent: :class:`.Agent` object to assign to this Listing
        :param str listing_id: id of the listing.
        :param str asset_did: the asset DID for this listing
        :param data: data of the listing
        :param ddo: Optional DDO object for this listing
        :type data: dict
    """
    def __init__(self, agent: AgentBase, listing_id: str, asset_did: str, data: Any, ddo: DDO = None) -> None:
        """init the the Listing Object Base with the agent instance"""
        self._agent = agent
        self._listing_id = listing_id
        self._asset_did = asset_did
        self._data = data
        self._ddo = ddo
        super().__init__()

    @abstractmethod
    def purchase(self, account: AccountBase) -> None:
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
    def agent(self) -> AgentBase:
        """

        :return: Agent object that created this listing
        :type: :class:`.SquidAgent`
        """
        return self._agent

    @property
    def data(self) -> Any:
        """

        :return: data of the listing
        :type: dict or None
        """
        return self._data

    @property
    def ddo(self) -> DDO:
        """

        :return: ddo of the listing
        :type: dict or None
        """
        return self._ddo

    @property
    def listing_id(self) -> str:
        """

        :return: the listing id
        :type: str or None
        """
        return self._listing_id

    @property
    def asset_did(self) -> str:
        """

        :return: asset DID held by the listing
        :type: str
        """
        return self._asset_did

    @property
    def did(self) -> str:
        """

        :return: asset held did
        :type: str
        """
        return self._asset_did

    @property
    def is_empty(self) -> bool:
        """

        Checks to see if this Listinng is empty.

        :return: True if this listing is empty else False.
        :type: boolean
        """
        return self._listing_id is None or self._asset_did is None
