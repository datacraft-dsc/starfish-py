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

    Account class, adds functionality for an account to be used on the starfish named network.

    :param address: address or dict of the account details
    :type address: string or dict
    :param password: password for the account
    :type password: str or None
    :param str key_value: key value data that is stored in the keyfile
    :param keyfile: keyfile containing the private encrypted key
    :type keyfile: str or None


    If the address parameter is a string then it's the account address.
    If dict then the dict can be the following format: ::

        {
            'address': 'xxxx',
            'password': 'yyyy',
        }

    """

    @abstractmethod
    def load_from_file(self, filename: str) -> None:
        """

        Load in a key value from a file

        :param str filename: file to that has the key_value

        """
        pass

    @abstractmethod
    def save_to_file(self, filename: str) -> None:
        """

        Save a key value to a file

        :param str filename: filename to write the key_value too.

        """
        pass

    @abstractmethod
    @property
    def export_key_value(self):
        """

        Export a key_value to json text

        """
        return None

    @abstractmethod
    def import_key_value(self, json_text: str) -> None:
        """

        Import a key_value from a json string

        """
        pass

    @abstractmethod
    def export_key(self, password: str) -> str:
        """

        Export the private key


        """
        return None

    @abstractmethod
    def import_key(self, raw_key: str, password: str) -> None:
        """

        Import the raw private key

        """
        pass

    @abstractmethod
    def is_address_equal(self, address: str) -> bool:
        """

        Compares two addresses if are equal. Both addresses are converted to checksum
        address and then compared.

        :param str address: address to compare with this object's address
        :return: True if the param address is the same is the one held in this account
        :type: bool

        >>> account = Account('0x00bd138abd70e2f00903268f3db08f2d25677c9e')
        >>> account.is_address_equal('0x00Bd138aBD70e2F00903268F3Db08f2D25677C9e')
        True
        """
        return False

    @abstractmethod
    def sign_transaction(self, web3: Any, transaction: Any) -> Any:
        pass

    @abstractmethod
    @property
    def is_password(self) -> bool:
        """
        Return True if the password has been set, else return False

        """
        return False

    @abstractmethod
    @property
    def address(self) -> str:
        """

        Return the account address for this account

        :return: address
        :type: str

        >>> account = Account('0x00bd138abd70e2f00903268f3db08f2d25677c9e')
        >>> account.address
        0x00bd138abd70e2f00903268f3db08f2d25677c9e
        """
        return None

    @abstractmethod
    @property
    def as_checksum_address(self) -> str:
        """

        Return the address as a checksum address

        :return: checksum address
        :type: str

        >>> account = Account('0x00bd138abd70e2f00903268f3db08f2d25677c9e')
        >>> account.as_checksum_address
        0x00Bd138aBD70e2F00903268F3Db08f2D25677C9e

        """
        return None

    @abstractmethod
    @property
    def password(self) -> str:
        """

        Return the account password for this account

        :return: password
        :type: str

        >>> account.password
        secret

        """
        return None

    def __str__(self) -> str:
        return f'Account: {self.address}'
