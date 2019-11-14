"""

Account class to provide basic functionality for all Ocean Accounts

"""

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

    def __init__(self, ocean, address, password=None, keyfile=None, agent_adapter=None):
        """init a standard ocean agent"""
        self._ocean = ocean
        self._address = None
        self._password = None
        self._agent_adapter = agent_adapter
        if self._agent_adapter is None:
            self._agent_adapter = self._ocean.get_squid_agent_adapter()


        if isinstance(address, dict):
            self._address = address.get('address')
            self._password = address.get('password')
            self._keyfile = address.get('keyfile')
        elif isinstance(address, (tuple, list)):
            self._address = address[0]
            if len(address) > 1:
                self._password = address[1]
            if len(address) > 2:
                self._keyfile = address[2]
        elif isinstance(address, str):
            self._address = address
            self._password = password
            self._keyfile = keyfile


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
        adapter = self.agent_adapter
        if adapter:
            return adapter.request_tokens(amount, self.agent_adapter_account)
        return 0

    def approve_tokens(self, spender_address, amount):
        """
        Approve some ocean tokens to be transfere from this account address by another Spender address

        :param number amount: The amount of ocean tokens to approve
        :param address spender_address: The address of spender
        :return: boolean
        """
        adapter = self.agent_adapter
        if adapter:
            amount = Web3.toWei(amount, 'ether')
            return adapter.approve_tokens(spender_address, amount, self)
        return False

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

        adapter = self.agent_adapter
        if adapter:
            return adapter.transfer_ether(self.agent_adapter_account, to_address, amount_wei)
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

        adapter = self.agent_adapter
        if adapter:
            return adapter.transfer_tokens(self.agent_adapter_account, to_address, amount_vodka)
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
    def key_file(self):
        """
        Compatability field, so that this account behaves the same as a squid account
        """
        return self._keyfile

    @property
    def is_valid(self):
        return self._address and self._password and self._keyfile

    @property
    def ocean_balance(self):
        """

        Get the number of ocean tokens

        :return: number of ocean tokens
        :type: number

        >>> account.ocean_balance
        101

        """
        adapter = self.agent_adapter
        if adapter:
            balance = adapter.get_account_balance(self.agent_adapter_account)
            if balance:
                return Web3.fromWei(balance.ocn, 'ether')
        return 0

    @property
    def ocean_balance_raw(self):
        """

        Get the number of ocean tokens

        :return: number of ocean tokens
        :type: number

        >>> account.ocean_balance_raw
        101

        """
        adapter = self.agent_adapter
        if adapter:
            balance = adapter.get_account_balance(self.agent_adapter_account)
            if balance:
                return balance.ocn
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
        adapter = self.agent_adapter
        if adapter:
            balance = adapter.get_account_balance(self.agent_adapter_account)
            if balance:
                return Web3.fromWei(balance.eth, 'ether')
        return 0

    @property
    def agent_adapter(self):
        return self._agent_adapter

    @agent_adapter.setter
    def agent_adapter(self, agent_adapter):
        self._agent_adapter = agent_adapter

    @property
    def agent_adapter_account(self):
        """

        Return the squid account object used for squid services, curretly only hosted accounts can be used
        :params obj adapter: middleware agent adapter to get the actual account object for this adapter
        :return: The squid account object
        :type: object

        """

        return self._agent_adapter.get_account(self.as_checksum_address, self._password, self._keyfile)

    def __str__(self):
        return f'Account: {self.address}'
