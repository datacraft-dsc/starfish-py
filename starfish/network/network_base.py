"""

    Network class

    To access block chain network services.

"""

import logging

from abc import (
    ABC,
    abstractmethod
)

from starfish.network.account_base import AccountBase
from starfish.network.ddo import DDO
from starfish.network.did import is_did
from starfish.types import Authentication

logger = logging.getLogger(__name__)


class NetworkBase(ABC):

    def __init__(self, url: str):
        self._url = url

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
                ddo = DDO.import_from_text(ddo_text)
            return ddo

        if not authentication:
            if username or password:
                authentication = {
                    'username': username,
                    'password': password
                }
        ddo_text = RemoteAgent.resolve_url(agent_url_did, authentication)
        if ddo_text:
            ddo = DDO.import_from_text(ddo_text)
        return ddo

    @property
    def url(self) -> str:
        return self._url
