"""

    Account class to provide basic functionality for all Starfish library accounts.

"""

import json
from typing import (
    Any,
    Generic
)

from eth_account import Account as EthAccount
from web3 import Web3

from starfish.types import TAccount


class EthereumAccount(Generic[TAccount]):
    """

    Account class, adds functionality for an account to be used on the starfish named network.

    :param address: address or dict of the account details
    :type address: string or dict
    :param password: password for the account
    :type password: str or None
    :param str key_data: key value data that is stored in the keyfile
    :param keyfile: keyfile containing the private encrypted key
    :type keyfile: str or None


    If the address parameter is a string then it's the account address.
    If dict then the dict can be the following format: ::

        {
            'address': 'xxxx',
            'password': 'yyyy',
        }

    """

    def __init__(self, password: str = None, key_data: Any = None, key_file: str = None) -> None:
        """init a standard account object"""
        self._password = None
        self._key_data = None
        self._address = None

        self._password = password
        self._set_key_data(key_data)

        # auto load in key_data from file
        if key_file:
            self.load_from_file(key_file)

    @staticmethod
    def create(password: str) -> TAccount:
        """

        Create a new account.

        You need to call `save_key_file` method to save the key information

        :return: Returns an account object
        """
        local_account = EthAccount.create(password)
        key_data = EthAccount.encrypt(local_account.key, password)
        account = EthereumAccount(password, key_data=key_data)
        return account

    def load_from_file(self, filename: str) -> None:
        """

        Load in a key value from a file

        :param str filename: file to that has the key_data

        """
        with open(filename, 'r') as fp:
            data = json.load(fp)
            self._set_key_data(data)

    def save_to_file(self, filename: str) -> None:
        """

        Save a key value to a file

        :param str filename: filename to write the key_data too.

        """
        if self._key_data:
            with open(filename, 'w') as fp:
                json.dump(self._key_data, fp)

    @property
    def export_as_text(self):
        """

        Export a key_data to json text

        """
        return json.dumps(self._key_data, sort_keys=True, indent=2)

    def import_from_text(self, json_text: str) -> None:
        """

        Import a key_data from a json string

        """
        data = json.loads(json_text)
        self._set_key_data(data)

    def export_private_key(self, password: str) -> str:
        """

        Export the private key


        """
        return EthAccount.decrypt(self._key_data, password)

    def import_key(self, raw_key: str, password: str) -> None:
        """

        Import the raw private key

        """
        self._set_key_data(EthAccount.encrypt(raw_key, password))

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
        return self.as_checksum_address == Web3.toChecksumAddress(address)

    def sign_transaction(self, web3: Any, transaction: Any) -> Any:
        if self._key_data:
            secret_key = web3.eth.account.decrypt(self._key_data, self._password)
            signed = web3.eth.account.sign_transaction(transaction, secret_key)
            return signed

    @property
    def is_password(self) -> bool:
        """
        Return True if the password has been set, else return False

        """
        return self._password is not None

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
        return self._address

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
        if self._address:
            return Web3.toChecksumAddress(self._address.lower())
        return None

    @property
    def password(self) -> str:
        """

        Return the account password for this account

        :return: password
        :type: str

        >>> account.password
        secret

        """
        return self._password

    @property
    def key_data(self) -> Any:
        """

        This is the encrypted key value that contains the account private key

        """
        return self._key_data

    @property
    def is_valid(self) -> bool:
        return self._address and self._password and self._key_data

    def _set_key_data(self, key_data):
        self._key_data = key_data
        if self._key_data:
            self._address = Web3.toChecksumAddress(self._key_data['address'])

    def __str__(self) -> str:
        return f'Account: {self.address}'
