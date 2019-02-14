"""

Agent class to provide basic functionality for all Ocean Agents

"""

from starfish import (
    Account,
)

from starfish.models.squid_model import SquidModel
from starfish.agent import AgentObject
from starfish.listing import SquidListing


class SquidAgent(AgentObject):
    """

    Squid Agent class allows to register and list asset listings.

    :param ocean: Ocean object that is being used.
    :type ocean: :class:`starfish.Ocean`
    :param aquarius_url: Aquarius url ( http://localhost:5000 ).
    :type aquarius_url: str or None
    :param brizo_url: Brizo url (http://localhost:8030).
    :type brizo_url: str or None
    :param secret_store_url: Secret store URL (http://localhost:8010).
    :type secret_store_url: str or None
    :param parity_url: Parity URL, if you are using the secret store (http://localhost:9545').
    :type parity_url: str or None
    :param storage_path: Path to the storage db (squid_py.db).
    :type storage_path: str or None

    Example how to use this agent: ::

        # First import the classes
        from starfish.SquidAgent import SquidAgent
        from starfish import Ocean

        # create the ocean object
        ocean = Ocean()

        # get your publisher account
        account = ocean.get_account('0x00bd138abd70e2f00903268f3db08f2d25677c9e')

        #create the SquidAgent
        my_config = {
            'aquarius_url': 'http://localhost:5000',
            'brizo_url': 'http://localhost:8030',
            'secret_store_url': 'http://localhost:12001',
            'parity_url': 'http://localhost:9545',
            'storage_path': 'squid_py.db',
        }
        agent = SquidAgent(ocean, my_config)

        # register an asset data and listing info
        listing = agent.register(metadata, account)
    """

    def __init__(self, ocean, *args, **kwargs):
        """init a standard ocean object"""
        AgentObject.__init__(self, ocean)
        self._model = None

        if args and isinstance(args[0], dict):
            kwargs = args[0]

        self._aquarius_url = kwargs.get('aquarius_url', 'http://localhost:5000')
        self._brizo_url = kwargs.get('brizo_url', 'http://localhost:8030')
        self._secret_store_url = kwargs.get('secret_store_url', 'http://localhost:12001')
        self._storage_path = kwargs.get('storage_path', 'squid_py.db')

    def register(self, metadata, account):
        """

        Register a squid asset with the ocean network.

        :param dict metadata: metadata dictionary to store for this asset.
        :param object account: Ocean account to use to register this asset.

        :return: A new :class:`.Asset` object that has been registered, if failure then return None.
        :type: :class:`.Asset` class

        For example::

            metadata = json.loads('my_metadata')
            # get your publisher account
            account = ocean.get_account('0x00bd138abd70e2f00903268f3db08f2d25677c9e')
            agent = SquidAgent(ocean)
            listing = agent.register_asset(metadata, account)

            if listing:
                print(f'registered my listing asset for sale with the did {listing.did}')

        """

        if not isinstance(account, Account):
            raise TypeError('You need to pass an Account object')

        if not account.is_valid:
            raise ValueError('You must pass a valid account')

        model = self.squid_model

        ddo = model.register_asset(metadata, account)
        listing = None
        if ddo:
            listing = SquidListing(self, metadata=ddo)

        return listing


    def get_listing(self, did):
        """

        Return an listing on the listing's DID.

        :param str did: DID of the listing.

        :return: a registered asset given a DID of the asset
        :type: :class:`.Asset` class

        """
        listing = None
        if SquidListing.is_did_valid(did):
            listing = SquidListing(self, did)
        else:
            raise ValueError(f'Invalid did "{did}" for an asset')

        return listing


    def search_listings(self, text, sort=None, offset=100, page=0):
        """

        Search the off chain storage for an asset with the givien 'text'

        :param str text: Test to search all metadata items for.
        :param sort: sort the results ( defaults: None, no sort).
        :type sort: str or None
        :param int offset: Return the result from with the maximum record count ( defaults: 100 ).
        :param int page: Returns the page number based on the offset.

        :return: a list of assets objects found using the search.
        :type: list of DID strings

        For example::

            # return the 300 -> 399 records in the search for the text 'weather' in the metadata.
            my_result = agent.search_registered_assets('weather', None, 100, 3)

        """
        model = self.squid_model
        ddo_list = model.search_assets(text, sort, offset, page)
        return ddo_list

    @property
    def squid_model(self):
        """

        Return an instance of the squid model, for access to the squid library layer
        :return: squid model object
        """

        if not self._model:
            options = {
                'aquarius_url': self._aquarius_url,
                'brizo_url': self._brizo_url,
                'secret_store_url': self._secret_store_url,
                'storage_path': self._storage_path,
            }
            self._model = SquidModel(self._ocean, options)
        return self._model
