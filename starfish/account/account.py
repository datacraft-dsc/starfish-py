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

from starfish.types import (
    AccountAddressOrDict,
    TAccount
)


class Account(Generic[TAccount]):
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

    def __init__(self, address: AccountAddressOrDict, password: str = None, key_value: Any = None, key_file: str = None) -> None:
        """init a standard account object"""
        self._address = None
        self._password = None
        self._key_value = None

        if isinstance(address, dict):
            self._address = Web3.toChecksumAddress(address.get('address'))
            self._password = address.get('password')
            self._key_value = address.get('key_value')
            key_file = address.get('key_file')
        elif isinstance(address, (tuple, list)):
            self._address = Web3.toChecksumAddress(address[0])
            if len(address) > 1:
                self._password = address[1]
            if len(address) > 2:
                self._key_value = address[2]
            if len(address) > 3:
                key_file = address[3]
        elif isinstance(address, str):
            self._address = Web3.toChecksumAddress(address)
            self._password = password
            self._key_value = key_value

        # auto load in key_value from file
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
        key_value = EthAccount.encrypt(local_account.key, password)
        account = Account(local_account.address, password, key_value)
        return account

    def load_from_file(self, filename: str) -> None:
        """

        Load in a key value from a file

        :param str filename: file to that has the key_value

        """
        with open(filename, 'r') as fp:
            self._key_value = json.load(fp)

    def save_to_file(self, filename: str) -> None:
        """

        Save a key value to a file

        :param str filename: filename to write the key_value too.

        """
        if self._key_value:
            with open(filename, 'w') as fp:
                json.dump(self._key_value, fp)

    @property
    def export_key_value(self):
        """

        Export a key_value to json text

        """
        return json.dumps(self._key_value, sort_keys=True, indent=2)

    def import_key_value(self, json_text: str) -> None:
        """

        Import a key_value from a json string

        """
        data = json.loads(json_text)
        self._key_value = data

    def export_key(self, password: str) -> str:
        """

        Export the private key


        """
        return EthAccount.decrypt(self._key_value, password)

    def import_key(self, raw_key: str, password: str) -> None:
        """

        Import the raw private key

        """
        self._key_value = EthAccount.encrypt(raw_key, password)

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
        if self.key_value:
            secret_key = web3.eth.account.decrypt(self.key_value, self._password)
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

    def set_password(self, password: str) -> None:
        """

        Set the password for this account

        :param str password: Password to set for this account

        >>> account.set_password('new secret')
        >>> account.password
        new secret
        """
        self._password = password

    @property
    def key_value(self) -> Any:
        """

        This is the encrypted key value that contains the account private key

        """
        return self._key_value

    @property
    def is_valid(self) -> bool:
        return self._address and self._password and self._key_value

    def __str__(self) -> str:
        return f'Account: {self.address}'
