"""

Account class to provide basic functionality for all Ocean Accounts

"""

from starfish.models.squid_model import SquidModel
from web3 import Web3

class Account():
    """

    Account class, adds functionality for an account to be used by the Ocean network.

    At the moment the Account object is created by the :class:`Ocean` class.

    :param ocean: Ocean object
    :type ocean: :class:`.Ocean`
    :param address: address or dict of the account details
    :type address: string or dict
    :param password: password for the account
    :type password: str or None

    If the address parameter is a string then it's the account address.
    If dict then the dict can be the following format: ::

        {
            'address': 'xxxx',
            'password': 'yyyy',
        }

    """

    def __init__(self, ocean, address, password=None):
        """init a standard ocean agent"""
        self._ocean = ocean
        self._address = None
        self._password = None
        self._unlock_squid_account = None

        if isinstance(address, dict):
            self._address = address.get('address')
            self._password = address.get('password')
        elif isinstance(address, (tuple, list)):
            self._address = address[0]
            if len(address) > 1:
                self._password = address[1]
        elif isinstance(address, str):
            self._address = address
            self._password = password

#        if isinstance(self._address, str):
#            self._address = add_0x_prefix(self._address)

    def unlock(self, password=None):
        """

        Unlock the account so that it can be used to spend tokens/gas

        :param password: optional password to use to unlock this account, if none provided then the original password will be used.

        :type password: str or None

        >>> account.unlock('secret')
        True

        """
        if password is None:
            password = self._password

        if password is None:
            raise ValueError('You must provide an account password to unlock')

        # clear out the onlocked account for squid
        self._unlock_squid_account = None
        self._unlock_squid_account = self._squid_account
        if self._unlock_squid_account:
            self._unlock_squid_account.password = password
            return True
        return False

    def lock(self):
        """

        Lock the account, to stop access to this account for ethereum token transfer

        :return: True if this account was unlocked, else False if the account was not locked.
        :type: boolean

        >>> account.lock()
        True
        """
        if self._unlock_squid_account:
            self._unlock_squid_account = None
            return True
        return False

    def request_tokens(self, amount):
        """

        For **Testing Only**

        Request some ocean tokens to be transfere to this account address

        :param number amount: The amount of ocean tokens to transfer ( *Money for nothing* )

        :return: number of tokens transfered
        :type: int

        >>> account.request_tokens(100)
        100
        """
        model = self._ocean.get_squid_model()
        if model:
            if not self._unlock_squid_account:
                raise ValueError('You must unlock the account before requesting tokens')

            return model.request_tokens(self._unlock_squid_account, amount)
        return 0

    def transfer_ether(self, to_account, amount_ether):
        """

        Transfer ether from this account to another account

        :param to_account: To account object or account address
        :type to_account: str for an account address or :class:'.Account` object

        ;param amount_ether: amount in ether to transfer
        :return: number of ether transfered

        """

        amount_wei = Web3.toWei(amount_ether, 'ether')
        to_address = to_account
        if isinstance(to_account, Account):
            to_address = to_account.address

        model = self._ocean.get_squid_model()
        if model:
            if not self._unlock_squid_account:
                raise ValueError('You must unlock the account before requesting tokens')

            return model.transfer_ether(self._unlock_squid_account, to_address, amount_wei)
        return 0

    def transfer_token(self, to_account, amount_token):
        """

        Transfer ocean tokens from this account to another account

        :param to_account: To account object or account address
        :type to_account: str for an account address or :class:'.Account` object

        ;param amount_ether: amount in ocean tokens to transfer
        :return: number of tokens transfered

        """

        amount_vodka = Web3.toWei(amount_token, 'ether')
        to_address = to_account
        if isinstance(to_account, Account):
            to_address = to_account.address

        model = self._ocean.get_squid_model()
        if model:
            if not self._unlock_squid_account:
                raise ValueError('You must unlock the account before requesting tokens')

            return model.transfer_tokens(self._unlock_squid_account, to_address, amount_vodka)
        return 0

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

    @property
    def ocean(self):
        """

        Return the :class:`.Ocean` object for this account
        :return: The main ocean class
        :type: :class:`.Ocean`

        """
        return self._ocean

    @property
    def is_hosted(self):
        """

        Return True if this account is registered in the Ocean network, on the block chain node
        :return: True if this account address is valid
        :type: boolean

        >>> account.is_hosted
        True
        """
        squid_account = self._squid_account
        return not squid_account is None

    @property
    def is_password(self):
        """
        Return True if the password has been set, else return False

        """
        return not self._password is None

    @property
    def _squid_account(self):
        """

        Return the squid account object used for squid services, curretly only hosted accounts can be used
        :return: The squid account object
        :type: object

        """

        if self._unlock_squid_account:
            return self._unlock_squid_account

        model = self._ocean.get_squid_model()
        if model:
            return model.get_account_host(self.as_checksum_address, self._password)
        return None

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
        self.lock()
        self._password = password

    @property
    def ocean_balance(self):
        """

        Get the number of ocean tokens

        :return: number of ocean tokens
        :type: number

        >>> account.ocean_balance
        101

        """
        model = self._ocean.get_squid_model()
        if model:
            squid_account = self._squid_account
            if squid_account:
                balance = model.get_account_balance(squid_account)
                if balance:
                    return Web3.fromWei(balance.ocn, 'ether')
        return 0

    @property
    def ether_balance(self):
        """

        Get the number of ocean tokens

        :return: number of ocean tokens
        :type: number

        >>> account.ether_balance
        1000000001867769600000000000

        """
        model = self._ocean.get_squid_model()
        if model:
            squid_account = self._squid_account
            if squid_account:
                balance = model.get_account_balance(self._squid_account)
                if balance:
                    return Web3.fromWei(balance.eth, 'ether')
        return 0

    def __str__(self):
        return f'Account: {self.address}'
