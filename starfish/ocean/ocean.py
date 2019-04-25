"""

Ocean class to access the Ocean eco system.

"""
import logging
import secrets

from web3 import (
    Web3,
    HTTPProvider
)

from starfish.account import Account
from starfish.models.squid_model import SquidModel

from starfish.logging import setup_logging


class Ocean():
    """
    .. _Asset class: asset.html
    .. _Config class: config.html

    The Ocean class connects to the ocean network.

    For example to use this class you can do the following: ::

        from starfish import Ocean

        my_config = {
            'contracts_path': 'artifacts',
            'keeper_url': 'http://localhost:8545',
            'gas_limit': 1000,
        }
        ocean = Ocean(my_config)

    or you can do the following setup: ::

        from starfish.ocean import Ocean
        ocean = Ocean(keeper_url='http://localhost:8545', contracts_path= artifacts, gas_limit=1000)

    or with no block chain network: ::

        from starfish.ocean import Ocean
        ocean = Ocean()



    You can provide these parameters in a dictionary or as individual parameters.

    :param keeper_url: url to the keeper node ( http://localhost:8545 ).
    :type keeper_url: str or None
    :param contracts_path: path to the contract files ( artifacts ).
    :type contracts_path: str or None
    :param gas_limit: The amount of gas you are willing to spend on each block chain transaction ( 0 ).
    :type gas_limit: int or string
    :param log_level: The log level to use for logging, the default is logging.DEBUG
    :type log_level: python logging level

    """

    def __init__(self, *args, **kwargs):
        """
        .. :class: starfish.Ocean

        init the basic Ocean class for the connection and contract info

        """
        if args and isinstance(args[0], dict):
            kwargs = args[0]

        self._keeper_url = kwargs.get('keeper_url', None)
        self._contracts_path = kwargs.get('contracts_path', None)
        self._gas_limit = kwargs.get('gas_limit', 0)
        setup_logging(level = kwargs.get('log_level', logging.WARNING))

        self.__web3 = None
        # For development, we use the HTTPProvider Web3 interface
        if self._keeper_url:
            self.__web3 = Web3(HTTPProvider(self._keeper_url))


        # default not to use squid
        self.__squid_model_class = None

        # only use squid or simiiar if we have the keeper url setup
        if self._keeper_url:
            self.__squid_model_class = kwargs.get('squid_model_class', SquidModel)


    def register_did(self, did, ddo, account):
        """

        Register this agent service with a DDO on the block chain.

        :param did: DID to use to register for this ddo.
        :type did: str or None
        :param ddo: DDO to save for the registration. This is a JSON string of a DDO
        :type string: JSON string of a DDO
        :param account: account to use as the owner of the registration.
        :type account: :class:`.Account`
        :return: the receipt of the block chain transaction
        :type: string

        For example::

            # register the public surfer on the block chain
            receipt = ocean.register_did(did, ddo.as_text(), register_account)

        TODO: Need to split this up into two calls, one to add, other to update
        """

        if not isinstance(account, Account):
            raise TypeError('You need to pass an Account object')

        if not account.is_valid:
            raise ValueError('You must pass a valid account')

        if not isinstance(ddo, str):
            raise TypeError('You need to pass a DDO as a string')

        # call the squid model to do the actual registration writing the ddo to the block chain
        model = self.get_squid_model()
        if model:
            return model.register_ddo(did, ddo, account)
        return None

    def resolve_did(self, did):
        """

        Return the resolved did written on the block chain
        if no value found then return None

        :param str did: did to resolve
        :return: ddo or url as a string
        :type: string

        """

        model = self.get_squid_model()
        if model:
            return model.resolve_did(did)
        return None

    def search_operations(self, text, limit=10):
        """

        Search the off chain storage for an operation that matches 'text'

        :param str text: Search for 'text' in metadata.
        :param int limit: Limit the result. If not provided, default is 10
        :return: a list of where each object is a 2-tuple (service provider did, operation did)
        :type: list of 2-tuple strings

        For example: ::

            # return the first 10 records in the search for operations that do model training
            #
            my_result = ocean.search_operations('model_training')
        """
        ## To be implemented
        return []

    def get_account(self, address, password=None):
        """
        Get an account object based on it's address

        :param address: address of the account, if dict then use the fields, `address` and `password`.
        :type address: str, list or dict
        :param password: optional password to save with the account
        :type password: str or None

        :return: return the :class:`Account` object or None if the account can not be used.
        :type: :class:`Account` or None

        >>> account = ocean.get_account('0x00bd138abd70e2f00903268f3db08f2d25677c9e')
        """
        account = Account(self, address, password)
        if account.is_valid:
            return account
        return None

    def create_account(self, password):
        """
        Create a new account object on the connected network. If the ocean object is
        not connected to a network, then a test address will be created

        :param password: optional password to save with the account
        :type password: str or None

        :return: return the :class:`Account` object or None if the account can not be used.
        :type: :class:`Account` or None

        >>> account = ocean.create_account('my_password')
        """
        account = None
        squid_model = self.get_squid_model()
        if squid_model:
            local_address = squid_model.create_account(password)
            if local_address:
                account = Account(self, local_address, password)
        else:
            address = secrets.token_hex(20)
            account = Account(self, address, password)

        return account

    @property
    def accounts(self):
        """
        :return: a list of :class:`.Account` objects
        :type: list of :class:`Account` objects

        >>> ocean.accounts
        {'0x00Bd138aBD70e2F00903268F3Db08f2D25677C9e': <starfish.account.Account object at 0x10456c080>, ...
        """
        model = self.get_squid_model()
        accounts = {}
        if model:
            for squid_account in model.accounts:
                account = Account(self, squid_account.address)
                accounts[account.address] = account
        return accounts

    @property
    def _web3(self):
        """return the web3 instance"""
        return self.__web3

    @property
    def keeper_url(self):
        return self._keeper_url

    @property
    def contracts_path(self):
        return self._contracts_path

    @property
    def gas_limit(self):
        return self._gas_limit

    def get_squid_model(self, options=None):
        if self.__squid_model_class:
            return self.__squid_model_class(self, options)
        return None
