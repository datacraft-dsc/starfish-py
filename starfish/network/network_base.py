"""

    Network class

    To access block chain network services.

"""

import logging

from abc import (
    ABC,
    abstractmethod
)
from typing import Any

from starfish.ddo import (
    DDO,
    create_ddo_object
)
from starfish.network.account_base import AccountBase
from starfish.types import (
    AccountAddress,
    Authentication
)
from starfish.utils.did import is_did

logger = logging.getLogger(__name__)


class NetworkBase(ABC):

    def __init__(self, url: str):
        self._url = url

    """

    Account based operations


    """

    @abstractmethod
    def get_token_balance(self, account_address: AccountAddress) -> float:
        return 0.0

    @abstractmethod
    def request_test_tokens(self, account: AccountBase, amount: float) -> bool:
        return False

    """

    Send tokens to another account

    """
    @abstractmethod
    def send_token(self, account: AccountBase, to_account_address: AccountAddress, amount: float) -> bool:
        return False

    """

    Send tokens (make payment) with logging

    """
    @abstractmethod
    def send_token_and_log(
        self,
        account: AccountBase,
        to_account_address: AccountAddress,
        amount: float,
        reference_1: str = None,
        reference_2: str = None
    ) -> bool:
        return False

    @abstractmethod
    def is_token_sent(
        self,
        from_account_address: AccountAddress,
        to_account_address: AccountAddress,
        amount: float,
        reference_1: str = None,
        reference_2: str = None
    ) -> bool:
        return False

    """

    Register Provenance

    """
    @abstractmethod
    def register_provenace(self, account: AccountBase, asset_id: str) -> bool:
        return False

    @abstractmethod
    def get_provenace_event_list(self, asset_id: str) -> Any:
        return False

    """

    Register DID with a DDO and resolve DID to a DDO

    """
    @abstractmethod
    def register_did(self, account: AccountBase, did: str, ddo_text: str) -> bool:
        return False

    @abstractmethod
    def resolve_did(self, did: str) -> str:
        return None

    """


    Helper methods


    """

    @abstractmethod
    def resolve_agent(
        self,
        agent_url_did: str,
        username: str = None,
        password: str = None,
        authentication: Authentication = None
    ) -> DDO:

        # stop circular references on import

        from starfish.agent.remote_agent import RemoteAgent

        ddo = None
        if is_did(agent_url_did):
            ddo_text = self.resolve_did(agent_url_did)
            if ddo_text:
                ddo = create_ddo_object(ddo_text)
            return ddo

        if not authentication:
            if username or password:
                authentication = {
                    'username': username,
                    'password': password
                }
        ddo_text = RemoteAgent.resolve_url(agent_url_did, authentication)
        if ddo_text:
            ddo = create_ddo_object(ddo_text)
        return ddo

    @property
    def url(self) -> str:
        return self._url
