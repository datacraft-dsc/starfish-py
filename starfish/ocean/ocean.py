"""

Ocean class to access the Ocean eco system.

"""
import logging

from starfish.utils.artifacts import (
    find_contract_path,
    is_contract_type_exists,
)

from web3 import (
    Web3,
    HTTPProvider
)

from starfish.account import Account
from starfish.middleware.squid_agent_adapter import SquidAgentAdapter
from squid_py.ocean.keeper import SquidKeeper


logger = logging.getLogger('starfish.ocean')

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

    :param network: name of the network to connect too. This can be 'development', 'nile' or 'kovan'
    :param keeper_url: url to the keeper node ( http://localhost:8545 ).
    :type keeper_url: str or None
    :param contracts_path: path to the contract files ( artifacts ).
        If not prodived then the network name will be used to search for the correct artifact files.
    :type contracts_path: str or None
    :param gas_limit: The amount of gas you are willing to spend on each block chain transaction ( 0 ).
    :type gas_limit: int or string

    """

    def __init__(self, *args, **kwargs):
        """
        .. :class: starfish.Ocean

        init the basic Ocean class for the connection and contract info

        """
        self.__web3 = None
        self.__squid_agent_adapter = None

        if args and isinstance(args[0], dict):
            kwargs = args[0]

        self._keeper_url = kwargs.get('keeper_url', None)
        self._network_name = kwargs.get('network', None)
        self._contracts_path = kwargs.get('contracts_path', None)
        self._gas_limit = kwargs.get('gas_limit', 0)
        self.__squid_agent_adapter_class = kwargs.get('squid_agent_adapter_class', None)

        if self._keeper_url and kwargs.get('connect', True):
            self.connect()

    def connect(self, keeper_url=None, network_name=None, contracts_path=None):
        """
        Normally you do not need to call this, since the ocean class will connect automatically
        using the provided keeper url and contracts path
        """
        if keeper_url:
            self._keeper_url = keeper_url
        if network_name:
            self._network_name = network_name
        if contracts_path:
            self._contracts_path = contracts_path

        if self._keeper_url:
            self.__web3 = Web3(HTTPProvider(self._keeper_url))
            # set the default squid adapter class if not set already
            if self.__squid_agent_adapter_class is None:
                self.__squid_agent_adapter_class = SquidAgentAdapter
            if not self._network_name:
                self._network_name = self._get_network_name()

        # check to see if the contracts path actually contain contracts for this network
        if self._contracts_path and not is_contract_type_exists(self._network_name, self._contracts_path):
            # if not then find the correct contracts path
            self._contracts_path = find_contract_path(self._network_name)
            logger.debug(f'Changing contracts path to {self._contracts_path}')

        # if no contracts path then search for the contract for this network
        if self._contracts_path is None and self._network_name:
            self._contracts_path = find_contract_path(self._network_name)

        logger.debug(f'network: {self._network_name} contracts_path: {self._contracts_path}')


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

            # register the public remote agent on the block chain
            receipt = ocean.register_did(did, ddo.as_text(), register_account)

        TODO: Need to split this up into two calls, one to add, other to update
        """

        if not isinstance(account, Account):
            raise TypeError('You need to pass an Account object')

        if not account.is_valid:
            raise ValueError('You must pass a valid account')

        if not isinstance(ddo, str):
            raise TypeError('You need to pass a DDO as a string')

        # call the squid adapter to do the actual registration writing the ddo to the block chain
        adapter = self.get_squid_agent_adapter()
        if adapter:
            return adapter.register_ddo(did, ddo, account.agent_adapter_account)
        return None

    def resolve_did(self, did):
        """

        Return the resolved did written on the block chain
        if no value found then return None

        :param str did: did to resolve
        :return: ddo or url as a string
        :type: string

        """

        adapter = self.get_squid_agent_adapter()
        if adapter:
            return adapter.resolve_did(did)
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

    def load_account(self, address, password=None, keyfile=None, agent_adapter=None):
        """
        Get an account object based on it's address, password and keyfile.
        This returns the account object, of the local account.

        :param address: address of the account, if dict then use the fields, `address`, `password` and 'keyfile'.
        :type address: str, list or dict
        :param str password: password to access the keyfile for this account
        :param str keyfile: JSON filename of the account key file.
        :param agent_adapter: Optional adapter class to use for this account object. Usually it's the :class:`SquidAdapter`

        :return: return the :class:`Account` object.
        :type: :class:`Account` or None

        >>> account = ocean.load_account('0x00bd138abd70e2f00903268f3db08f2d25677c9e', 'password', 'key_file_test.json')
        """
        account = Account(self, address, password, keyfile, agent_adapter)
        return account

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

    @property
    def network_name(self):
        return self._network_name

    @property
    def is_connected(self):
        return not self.__web3

    def _get_network_name(self):
        network_id = int(self.__web3.version.network)
        return SquidKeeper.get_network_name(network_id)

    def get_squid_agent_adapter(self, options=None):
        if self.__squid_agent_adapter_class:
            self.__squid_agent_adapter = self.__squid_agent_adapter_class(self, options)
            return self.__squid_agent_adapter
        return None
