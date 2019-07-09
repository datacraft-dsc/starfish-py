"""

Agent class to provide basic functionality for all Ocean Agents

"""


import datetime
import logging
import json

from web3 import Web3

from starfish.models.squid_model import SquidModel
from starfish.account import Account
from starfish.agent import AgentBase
from starfish.listing import Listing
from starfish.asset import (
    BundleAsset,
    FileAsset,
    RemoteAsset,
    Asset,
 )
from starfish.purchase import Purchase
from starfish.exceptions import StarfishPurchaseError
from starfish.models.squid_model import SquidModelPurchaseError
from starfish.utils.did import did_parse
from starfish.exceptions import StarfishAssetNotFound

from squid_py.brizo.brizo_provider import BrizoProvider
from squid_py.ddo.metadata import (
    MetadataBase,
    AdditionalInfoMeta,
)
from squid_py.exceptions import OceanDIDNotFound


logger = logging.getLogger('starfish.squid_agent')


ALLOWED_FILE_META_ITEMS = [
    'index',
    'url',
    'encoding',
    'compression',
    'checksum',
    'checksumType',
    'contentLength',
    'contentType',
    'resourceId',
]

class SquidAgent(AgentBase):
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
        AgentBase.__init__(self, ocean)
        self._model = None

        if args and isinstance(args[0], dict):
            kwargs = args[0]

        self._aquarius_url = kwargs.get('aquarius_url', 'http://localhost:5000')
        self._brizo_url = kwargs.get('brizo_url', 'http://localhost:8030')
        self._secret_store_url = kwargs.get('secret_store_url', 'http://localhost:12001')
        self._storage_path = kwargs.get('storage_path', 'squid_py.db')
        self._parity_url = kwargs.get('parity_url', self._ocean.keeper_url)

    def register_asset(self, asset, listing_data, account):
        """

        Register a squid asset with the ocean network.

        :param asset: the asset to register, at the moment only a SquidAsset can be used.
        :type asset: :class:`.FileAsset`, :class:`.RemoteAsset` or :class:`.BundleAsset` object to register
        :param dict listing_data: data that is required for listing a registered asset
        :param account: Ocean account to use to register this asset.
        :type account: :class:`.Account` object to use for registration.

        :return: A new :class:`.Listing` object that has been registered, if failure then return None.
        :type: :class:`.Listing` class

        At the moment only support FileAsset

        For example::

            metadata = json.loads('my_metadata')
            # get your publisher account
            account = ocean.get_account('0x00bd138abd70e2f00903268f3db08f2d25677c9e')
            agent = SquidAgent(ocean)
            asset = FileAsset(filename='Testfile.txt')
            listing = agent.register_asset(asset, {'price': 8}, account)

            if listing:
                print(f'registered my listing asset for sale with the did {listing.did}')

        """

        if not isinstance(account, Account):
            raise TypeError('You need to pass an Account object')

        if not account.is_valid:
            raise ValueError('You must pass a valid account')

        if not account.is_password:
            raise ValueError('You must set the account password')

        if not isinstance(listing_data, dict):
            raise TypeError('You must provide some listing data as dict')

        if not (isinstance(asset, FileAsset) or isinstance(asset, RemoteAsset) or isinstance(asset, BundleAsset)):
            raise TypeError('This agent only supports a FileAsset, RemoteAsset or BundleAsset')

        model = self.squid_model
        metadata = SquidAgent._convert_listing_asset_to_metadata(asset, listing_data)

        ddo = model.register_asset(metadata, account._squid_account)

        listing = None
        if ddo:
            asset.set_did(ddo.did)
            listing = Listing(self, ddo.did, asset, listing_data, ddo)

        return listing


    def validate_asset(self, asset):
        """

        Validate an asset

        :param asset: Asset to validate.
        :return: True if the asset is valid
        """

        if not asset:
            raise ValueError('asset must be an object')
        if not isinstance(asset, Asset):
            raise ValueErrer('asset must be a type of Asset object')
        if not asset.metadata:
            raise ValueError('Metadata must have a value')
        if not isinstance(asset.metadata, dict):
            raise ValueError('Metadat must be a dict')

        model = self.squid_model
        return model.validate_metadata(asset.metadata)

    def get_listing(self, listing_id):
        """
        Return an listing from the given listing_id.

        :param str listing_id: Id of the listing.

        :return: a registered listing given a Id of the listing
        :type: :class:`.Listing` class

        :raise: :class:`.StarfishAssetNotFound` if the asset is not found in
        aquarius or the DID of the asset is not on the network ( Block chain )
        """
        listing = None
        model = self.squid_model

        try:
            ddo = model.read_asset(listing_id)
        except OceanDIDNotFound as e:
            raise StarfishAssetNotFound(e)

        if ddo:
            listing = self._listing_from_ddo(ddo)
        return listing


    def search_listings(self, text, sort=None, offset=100, page=1):
        """

        Search the off chain storage for an asset with the givien 'text'

        :param str, dict text: Test to search all metadata items for. If the field is a string
        then the search will be a basic search, else a dict then a query will be performed
        :param sort: sort the results ( defaults: None, no sort).
        :type sort: str or None
        :param int offset: Return the result from with the maximum record count ( defaults: 100 ).
        :param int page: Returns the page number based on the offset ( defaults: 1 ).

        :return: a list of assets objects found using the search.
        :type: list of DID strings

        For example::

            # return the 300 -> 399 records in the search for the text 'weather' in the metadata.
            my_result = agent.search_registered_assets('weather', None, 100, 3)

        """
        model = self.squid_model
        if isinstance(text, str) or isinstance(text, dict):
            ddo_list = model.search_assets(text, sort, offset, page)
        else:
            raise ValueError('You can only pass a str or dict for the search text')
        result = []
        for ddo in ddo_list:
            listing = self._listing_from_ddo(ddo)
            result.append(listing)

        return result

    def purchase_asset(self, listing, account):
        """

        Purchase an asset using it's listing and an account.

        :param listing: Listing to use for the purchase.
        :type listing: :class:`.Listing`
        :param account: Ocean account to purchase the asset.
        :type account: :class:`.Account` object to use for registration.

        :raise: :class:`.StarfishAssetNotFound` if the asset is not found in
        aquarius or the DID of the asset is not on the network ( Block chain )

        """
        purchase = None
        model = self.squid_model

        try:
            service_agreement_id = model.purchase_asset(listing.ddo, account._squid_account)
        except OceanDIDNotFound as e:
            raise StarfishAssetNotFound(e)

        purchase = Purchase(self, listing, service_agreement_id, account)

        return purchase

    def is_access_granted_for_asset(self, asset, account, purchase_id=None ):
        """

        Check to see if the account and purchase_id have access to the assed data.


        :param asset: Asset to check for access.
        :type asset: :class:`.Asset` object
        :param account: Ocean account to purchase the asset.
        :type account: :class:`.Account` object to use for registration.
        :param str purchase_id: Optional purchase id that was used to purchase the asset.

        :return: True if the asset can be accessed and consumed.
        :type: boolean
        """

        model = self.squid_model

        if purchase_id:
            return model.is_access_granted_for_asset(asset.did, account._squid_account, purchase_id)
        else:
            purchase_id_list = model.get_asset_purchase_ids(asset.did)
            for purchase_id in purchase_id_list:
                if model.is_access_granted_for_asset(asset.did, account._squid_account, purchase_id):
                    return True
        return False

    def get_asset_purchase_ids(self, asset):
        """

        Returns as list of purchase id's that have been used for this asset

        :param asset: Asset to return purchase details.
        :type asset: :class:`.Asset` object

        :return: list of purchase ids
        :type: list

        """
        model = self.squid_model

        return model.get_asset_purchase_ids(asset.did)



    def purchase_wait_for_completion(self, asset, account, purchase_id, timeoutSeconds):
        """

        Wait for completion of the purchase

        TODO: issues here...
        + No method as yet to pass back paramaters and values during the purchase process
        + We assume that the following templates below will always be used.


        :param integer timeoutSeconds: Optional seconds to waif to purchase to complete. Default: 60 seconds
        :return: True if successfull or an error message if failed
        :type: string or boolean

        :raises OceanPurchaseError: if the correct events are not received

        """
        model = self.squid_model
        if not purchase_id:
            raise ValueError('Please provide a valid purhase id')

        try:
            model.purchase_wait_for_completion(asset.did, account._squid_account, purchase_id, timeoutSeconds)
        except SquidModelPurchaseError as purchaseError:
            raise StarfishPurchaseError(purchaseError)
        except Exception as e:
            raise e
        return True


    def consume_asset(self, listing, account, purchase_id):
        """

        Consume the asset and download the data. The actual payment to the asset
        provider will be made at this point.

        :param listing: Listing that was used to make the purchase.
        :type listing: :class:`.Listing`
        :param str purchase_id: purchase id that was used to purchase the asset.
        :param account: Ocean account that was used to purchase the asset.
        :type account: :class:`.Account` object to use for registration.
        :param str download_path: path to store the asset data.

        :return: BunleAsset object if you have purchased this asset, which contains one or more RemoteAssets
        :type: :class:`.BundleAsset`

        """
        asset = None
        model = self.squid_model
        file_list = model.consume_asset(listing.ddo, account._squid_account, purchase_id)
        if file_list:
            asset = BundleAsset(did=listing.ddo.did)
            for index, file_item in enumerate(file_list):
                asset_item = RemoteAsset(file_item, listing.ddo.did)
                asset.add(f'file_{index}', asset_item)
        return asset

    def watch_provider_events(self, account):
        """

        The provider or publisher needs to watch the events on the block chain, to
        then setup the agreement contracts on the block chain when the consume
        first starts to make the initial consume request ( payment to escrow ).

        :param account: Account to watch for payment events for the provider of the asset
        :type account: :class:`.Account`

        """
        model = self.squid_model
        model.watch_provider_events(account)

    def _listing_from_ddo(self, ddo):
        """ convert a ddo to a listing that contains a BundleAsset """

        listing_data, asset_metadata = self._convert_ddo_to_listing_data_asset_metadata(ddo)
        asset = BundleAsset(did=ddo.did)
        for index, asset_metadata_item in enumerate(asset_metadata):
            asset.add(f'file_{index}', RemoteAsset(metadata=asset_metadata_item, did=ddo.did))
        listing_id = ddo.did
        listing = Listing(self, listing_id, asset, listing_data, ddo)
        return listing

    @staticmethod
    def _convert_ddo_to_listing_data_asset_metadata(ddo):
        listing_data = ddo.metadata.get(MetadataBase.KEY, None)
        # put back additional fields that cannot be saved with the squid
        # main metadata

        # first copy the price from the network as the '' price ( in vodka's )
        listing_data['price_vodka'] = int(listing_data['price'])
        # all starfish prices are in ocean tokens - so convert from Vodka's to Ocean tokens
        listing_data['price'] = Web3.fromWei(int(ddo.metadata[MetadataBase.KEY]['price_vodka']), 'ether')
        asset_metadata = []
        if listing_data['files']:
            for file_data in listing_data['files']:
                asset_metadata.append(file_data)

        info = ddo.metadata.get(AdditionalInfoMeta.KEY, None)
        if info and isinstance(info, dict):
            for name, value in info.items():
                # for convinience we will try to decode 'extra_data' field as a json to dict
                try:
                    if name == 'extra_data' and isinstance(value, str):
                        value = json.loads(value)
                except json.decoder.JSONDecodeError:
                    pass
                listing_data[name] = value
        return listing_data, asset_metadata

    @staticmethod
    def _convert_listing_asset_to_metadata(asset, listing_data):
        """
        For squid we need to create a single metadata record from a listing_data and asset/s
        """
        metadata = {
            MetadataBase.KEY: {
                'name': 'Asset',
                'type': 'dataset',
                'dateCreated': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
                'author': 'Author',
                'license': 'closed',
                'price': '0',
                'files': []
            },
            AdditionalInfoMeta.KEY: {}
        }
        for name, value in listing_data.items():
            if name in MetadataBase.VALUES_KEYS:
                metadata[MetadataBase.KEY][name] = value
            else:
                metadata[AdditionalInfoMeta.KEY][name] = value


        # make sure we are sending a price value as string for squid in vodka
        metadata[MetadataBase.KEY]['price'] = str(Web3.toWei(metadata[MetadataBase.KEY]['price'], 'ether'))

        def append_asset_file(metadata, asset):
            metadata['base']['files'].append(asset.metadata)
            index = len(metadata['base']['files']) - 1
            metadata['base']['files'][index]['index'] = index
            if asset.is_asset_type('file'):
                metadata['base']['files'][index]['url'] = asset.metadata['filename']

        if isinstance(asset, BundleAsset):
            for _, asset_item in asset:
                if not (isinstance(asset_item, FileAsset) or isinstance(asset_item, RemoteAsset)):
                    raise TypeError(f'Invalid asset type {type(asset_item)}: The BundleAsset can only contain multilple assets of the type FileAsset or RemoteAsset')
                append_asset_file(metadata, asset_item)
        else:
            append_asset_file(metadata, asset)

        for item in metadata['base']['files']:
            delete_list = []
            for name in item.keys():
                if not name in ALLOWED_FILE_META_ITEMS:
                    delete_list.append(name)
            for name in delete_list:
                metadata[AdditionalInfoMeta.KEY][f'file_{name}'] = item[name]
                del item[name]
        return metadata


    @staticmethod
    def invoke_operation(listing, account, purchase_id, payload):
        """
        Invoke the operation

        :param listing: Listing that was used to make the purchase.
        :type listing: :class:`.Listing`
        :param account: Ocean account that was used to purchase the asset.
        :type account: :class:`.Account` object to use for registration.
        :param str purchase_id: purchase id that was used to purchase the asset.
        :param str payload: params required for the operation

        :return: True if the operation was invoked
        :type: boolean

        """
        logger.info(f'calling invoke in squid_agent.py with payload: {payload}')
        try :
            ddo= listing.data
            files = ddo.metadata['base']['encryptedFiles']
            logger.info(f'encrypted contentUrls: {files}')
            files = files if isinstance(files, str) else files[0]
            sa = SquidModel.get_service_agreement_from_ddo(ddo)
            service_url = sa.service_endpoint
            if not service_url:
                logger.error(
                    'Consume asset failed, service definition is missing the "serviceEndpoint".')
                raise AssertionError(
                    'Consume asset failed, service definition is missing the "serviceEndpoint".')

            return BrizoProvider.get_brizo().invoke_service(
                purchase_id, service_url,
                account.address, payload)
        except Exception:
            logger.error('got error invoking Brizo')
            traceback.print_exc(file=sys.stdout)
            return False



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
                'parity_url': self._parity_url,
                'storage_path': self._storage_path,
            }
            self._model = self._ocean.get_squid_model(options)
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
