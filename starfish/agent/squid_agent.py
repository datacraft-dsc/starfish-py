"""

Agent class to provide basic functionality for all Ocean Agents

"""



from starfish.models.squid_model import SquidModel
from starfish.account import Account
from starfish.agent import Agent
from starfish.listing import Listing
from starfish.asset import Asset
from starfish.purchase import Purchase
from starfish.utils.did import did_parse


class SquidAgent(Agent):
    """

    Squid Agent class allows to register and list asset listings.

    :param ocean: Ocean object that is being used.
    :type ocean: :class:`.Ocean`
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
        from starfish.agent import SquidAgent
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
        Agent.__init__(self, ocean)
        self._model = None

        if args and isinstance(args[0], dict):
            kwargs = args[0]

        self._aquarius_url = kwargs.get('aquarius_url', 'http://localhost:5000')
        self._brizo_url = kwargs.get('brizo_url', 'http://localhost:8030')
        self._secret_store_url = kwargs.get('secret_store_url', 'http://localhost:12001')
        self._storage_path = kwargs.get('storage_path', 'squid_py.db')

    def register_asset(self, metadata, account):
        """

        Register a squid asset with the ocean network.

        :param dict metadata: metadata dictionary to store for this asset.
        :param account: Ocean account to use to register this asset.
        :type account: :class:`.Account` object to use for registration.

        :return: A new :class:`.Listing` object that has been registered, if failure then return None.
        :type: :class:`.Listing` class

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

        ddo = model.register_asset(metadata, account._squid_account)

        listing = None
        if ddo:
            asset = Asset(metadata, ddo.did)
            listing = Listing(self, ddo.did, asset, ddo)

        return listing


    def get_listing(self, did):
        """

        Return an listing on the listing's DID.

        :param str did: DID of the listing.

        :return: a registered asset given a DID of the asset
        :type: :class:`.Asset` class

        """
        listing = None
        if SquidAgent.is_did_valid(did):
            model = self.squid_model
            ddo = model.read_asset(did)

            if ddo:
                asset = Asset(ddo.metadata, ddo.did)
                listing = Listing(self, ddo.did, asset, ddo)
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

    def purchase_asset(self, listing, account):
        """

        Purchase an asset using it's listing and an account.

        :param listing: Listing to use for the purchase.
        :type listing: :class:`.Listing`
        :param account: Ocean account to purchase the asset.
        :type account: :class:`.Account` object to use for registration.

        """
        purchase = None
        model = self.squid_model

        service_agreement_id = model.purchase_asset(listing.data, account._squid_account)
        if service_agreement_id:
            purchase = Purchase(self, listing, service_agreement_id)

        return purchase

    def is_access_granted_for_asset(self, asset, purchase_id, account):
        """

        Check to see if the account and purchase_id have access to the assed data.


        :param asset: Asset to check for access.
        :type asset: :class:`.Asset` object
        :param str purchase_id: purchase id that was used to purchase the asset.
        :param account: Ocean account to purchase the asset.
        :type account: :class:`.Account` object to use for registration.

        :return: True if the asset can be accessed and consumed.
        :type: boolean
        """

        model = self.squid_model
        return model.is_access_granted_for_asset(asset.did, purchase_id, account._squid_account)


    def consume_asset(self, listing, purchase_id, account, download_path ):
        """
        Consume the asset and download the data. The actual payment to the asset
        provider will be made at this point.

        :param listing: Listing that was used to make the purchase.
        :type listing: :class:`.Listing`
        :param str purchase_id: purchase id that was used to purchase the asset.
        :param account: Ocean account that was used to purchase the asset.
        :type account: :class:`.Account` object to use for registration.
        :param str download_path: path to store the asset data.

        :return: True if the asset has been consumed and downloaded
        :type: boolean

        """
        model = self.squid_model
        return model.consume_asset(listing.data, purchase_id, account._squid_account, download_path)

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

    @staticmethod
    def is_did_valid(did):
        """
        Checks to see if the DID string is a valid DID for this type of Asset.
        This method only checks the syntax of the DID, it does not resolve the DID
        to see if it is assigned to a valid Asset.

        :param str did: DID string to check to see if it is in a valid format.

        :return: True if the DID is in the format 'did:op:xxxxx'
        :type: boolean
        """
        data = did_parse(did)
        return not data['path']
