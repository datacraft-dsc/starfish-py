"""

    Account class to provide basic functionality for all Starfish library accounts.

"""

from web3 import Web3


class Account():
    """

    Account class, adds functionality for an account to be used on the starfish named network.

    :param address: address or dict of the account details
    :type address: string or dict
    :param password: password for the account
    :type password: str or None
    :param keyfile: keyfile containing the private encrypted key
    :type keyfile: str or None

    If the address parameter is a string then it's the account address.
    If dict then the dict can be the following format: ::

        {
            'address': 'xxxx',
            'password': 'yyyy',
        }

    """

    def __init__(self, address, password=None, keyfile=None):
        """init a standard ocean agent"""
        self._address = None
        self._password = None

        if isinstance(address, dict):
            self._address = Web3.toChecksumAddress(address.get('address'))
            self._password = address.get('password')
            self._keyfile = address.get('keyfile')
        elif isinstance(address, (tuple, list)):
            self._address = Web3.toChecksumAddress(address[0])
            if len(address) > 1:
                self._password = address[1]
            if len(address) > 2:
                self._keyfile = address[2]
        elif isinstance(address, str):
            self._address = Web3.toChecksumAddress(address)
            self._password = password
            self._keyfile = keyfile

    def is_address_equal(self, address):
        """

        Compares two addresses if are equal. Both addresses are converted to checksum
        address and then compared.

        :param str address: address to compare with this object's address
        :return: True if the param address is the same is the one held in this account
        :type: boolean

        >>> account = ocean.get_account('0x00bd138abd70e2f00903268f3db08f2d25677c9e')
        >>> account.is_address_equal('0x00Bd138aBD70e2F00903268F3Db08f2D25677C9e')
        True
        """
        return self.as_checksum_address == Web3.toChecksumAddress(address)

    def sign_transaction(self, web3, transaction):
        encrypted_key = None
        with open(self._keyfile, 'r') as fp:
            encrypted_key = fp.read()
        if encrypted_key:
            secret_key = web3.eth.account.decrypt(encrypted_key, self._password)
            signed = web3.eth.account.sign_transaction(transaction, secret_key)
            return signed

    @property
    def is_password(self):
        """
        Return True if the password has been set, else return False

        """
        return self._password is not None

    @property
    def address(self):
        """

        Return the account address for this account

        :return: address
        :type: str

        >>> account = ocean.get_account('0x00bd138abd70e2f00903268f3db08f2d25677c9e')
        >>> account.address
        0x00bd138abd70e2f00903268f3db08f2d25677c9e
        """
        return self._address

    @property
    def as_checksum_address(self):
        """

        Return the address as a checksum address

        :return: checksum address
        :type: str

        >>> account = ocean.get_account('0x00bd138abd70e2f00903268f3db08f2d25677c9e')
        >>> account.as_checksum_address
        0x00Bd138aBD70e2F00903268F3Db08f2D25677C9e

        """
        if self._address:
            return Web3.toChecksumAddress(self._address.lower())
        return None

    @property
    def password(self):
        """

        Return the account password for this account

        :return: password
        :type: str

        >>> account.password
        secret

        """
        return self._password

    def set_password(self, password):
        """

        Set the password for this account

        :param str password: Password to set for this account

        >>> account.set_password('new secret')
        >>> account.password
        new secret
        """
        self._password = password

    @property
    def keyfile(self):
        return self._keyfile

    @property
    def is_valid(self):
        return self._address and self._password and self._keyfile

    def __str__(self):
        return f'Account: {self.address}'
