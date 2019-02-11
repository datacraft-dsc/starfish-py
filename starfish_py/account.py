"""

Account class to provide basic functionality for all Ocean Accounts

"""

class Account():
    """

    Account class, adds functionality for an account to be used by the Ocean network.

    At the moment the Account object in created by the :class:`Ocean` class.

    :param ocean: Ocean object
    :type ocean: :class:`.Ocean`
    :param address: address or dict of the account details
    :type address: string or dict
    :param password: password for the account
    :type password: str or None

    If the address parameter is a string then it's the account address, if dict then the format:
        'address': 'xxx',
        'password': 'xxx'

    """

    def __init__(self, ocean, address, password=None):
        """init a standard ocean agent"""
        self._ocean = ocean
        self._address = None
        self._password = None
        self._unlock_squid_account = None

        if isinstance(address, dict):
            self.set_address(address.get('address'))
            self._password = address.get('password')
        elif isinstance(address, str):
            self.set_address(address)
            self._password = password

    def unlock(self, password=None):
        """

        Unlock the account so that it can be used to spend tokens/gas

        :param password: optional password to use to unlock this account, if none provided then the original password will be used.

        :type password: str or None

        """
        if password is None:
            password = self._password

        if password is None:
            raise ValueError('You must provid an account password to unlock')

        # clear out the onlocked account for squid
        self._unlock_squid_account = None
        self._unlock_squid_account = self._squid_account
        if self._unlock_squid_account:
            self._unlock_squid_account.password = password
            self._unlock_squid_account.unlock()

    def lock(self):
        """

        Lock the account, to stop access to this account for token transfer

        :return: True if this account was unlocked, else False
        :type: boolean

        """
        if self._unlock_squid_account:
            self._unlock_squid_account = None
            return True
        return False

    def request_tokens(self, amount):
        """

        For **Testing Only**

        Request some ocean tokens to be transfere to this account address

        :return: number of tokens transfered
        :type: int
        """
        squid_account = self._squid_account
        if squid_account:
            return squid_account.request_tokens(amount)
        return 0

    def is_address_equal(self, address):
        """

        Compares two addresses if are equal. Both addresses are converted to checksum
        address and then compared

        :param str address: address to compare with this object's address
        :return: True if the param address is the same is the one held in this account
        :type: boolean

        """
        return self.as_checksum_address == self._ocean._web3.toChecksumAddress(address)

    @property
    def is_valid(self):
        """

        Return True if this account is registered in the Ocean network
        :return: True if this account address is valid
        :type: boolean

        """
        squid_account = self._squid_account
        return not squid_account is None

    @property
    def _squid_account(self):
        """

        Return the squid account object used for squid services
        :return: The squid account object
        :type: object

        """

        if self._unlock_squid_account:
            return self._unlock_squid_account
        else:
            address = self.as_checksum_address
            if self._address:
                account_list = self._ocean._squid.get_accounts()
                if address in account_list:
                    return account_list[address]
        return None

    @property
    def address(self):
        """

        Return the account address for this account
        :return: address
        :type: str
        """
        return self._address

    @property
    def as_checksum_address(self):
        """

        Return the address as a checksum address
        :return: checksum address
        :type: str
        """
        if self._address:
            return self._ocean._web3.toChecksumAddress(self._address.lower())
        return None

    def set_address(self, address):
        """

        Sets the address and converts the address to a ethereum checksum address

        :param str address: new address to set for this account

        """
        self._address = address

    @property
    def password(self):
        """

        Return the account password for this account
        :return: password
        :type: str
        """
        return self._password

    def set_password(self, password):
        """

        Set the password for this account

        :param str password: Password to set for this account

        """
        self.lock()
        self._password = password

    @property
    def ocean_balance(self):
        """

        Get the number of ocean tokens

        :return: number of ocean tokens
        :type: number
        """
        squid_account = self._squid_account
        if squid_account:
            return squid_account.ocean_balance
        return 0


    @property
    def ether_balance(self):
        """

        Get the number of ocean tokens

        :return: number of ocean tokens
        :type: number
        """
        squid_account = self._squid_account
        if squid_account:
            return squid_account.ether_balance
        return 0
