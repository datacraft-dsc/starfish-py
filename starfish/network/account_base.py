"""

    Account class to provide basic functionality for all Starfish library accounts.

"""

from abc import (
    ABC,
    abstractmethod
)

from typing import Any


class AccountBase(ABC):
    """

    Base Account class


    """

    @abstractmethod
    def sign_transaction(self, transaction: Any) -> Any:
        pass
