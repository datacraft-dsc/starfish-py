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

    Squid Agent class allows to connect to the ocean squid library and perform asset based tasks.
    
    'aquarius_url': 'http://localhost:5000',
    'brizo_url': 'http://localhost:8030',
    'secret_store_url': 'http://localhost:8010',
    'parity_url': 'http://localhost:9545',
    'storage_path = squid_py.db',

    """

    def __init__(self, ocean, *args, **kwargs):
        """init a standard ocean object"""
        AgentObject.__init__(self, ocean)
        self._model = None

        if args and len(args) > 0 and isinstance(args[0], dict):
            kwargs = args[0]

        self._aquarius_url = kwargs.get('aquarius_url', 'http://localhost:5000')
        self._brizo_url = kwargs.get('brizo_url', 'http://localhost:8030')
        self._secret_store_url = kwargs.get('secret_store_url', 'http://localhost:12001')
        self._storage_path = kwargs.get( 'storage_path', 'squid_py.db')

    def register(self, metadata, account):
        """

        Register a squid asset with the ocean network.

        :param dict metadata: metadata dictionary to store for this asset.
        :param object account: Ocean account to use to register this asset.

        :return: A new :class:`.Asset` object that has been registered, if failure then return None.
        :type: :class:`.Asset` class

        For example::

            metadata = json.loads('my_metadata')
            account = ocean.accounts[0]
            asset = ocean.register_asset(metadata, account)
            if asset:
                print(f'registered my asset with the did {asset.did}')

        """

        if not isinstance(account, Account):
            raise TypeError('You need to pass an Account object')

        if not account.is_valid:
            raise ValueError('You must pass a valid account')

        model = self.squid_model

        ddo = model.register_asset(metadata, account)
        listing = None
        if ddo:
            listing = SquidListing(self, ddo=ddo)

        return listing


    def get_listing(self, did):
        """

        Return an listing on the listing's DID.

        :param str did: DID of the asset and agent combined.

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
            my_result = ocean.search_registered_assets('weather', None, 100, 3)

        """
        asset_list = None
        model = self.squid_model
        ddo_list = model.search_assets(text, sort, offset, page)
        return ddo_list

    @property
    def squid_model(self):
        if not self._model:
            options = {
                'aquarius_url': self._aquarius_url,
                'brizo_url': self._brizo_url,
                'secret_store_url': self._secret_store_url,
                'storage_path': self._storage_path,
            }
            self._model = SquidModel(self._ocean, options)
        return self._model
