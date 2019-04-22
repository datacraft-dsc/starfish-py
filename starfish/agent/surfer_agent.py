"""

Surfer Agent class to provide basic functionality for Ocean Agents

In starfish-java, this is named as `RemoteAgent`

"""
import secrets
import re
import json

from starfish.account import Account
from starfish.agent import AgentBase
from starfish.asset import MemoryAsset
from starfish.models.surfer_model import SurferModel
from starfish.models.squid_model import SquidModel
from starfish.asset import Asset
from starfish.utils.did import did_parse
from starfish.listing import Listing



from squid_py.ddo.ddo import DDO

class SurferAgent(AgentBase):
    """

    Surfer Agent class allows to register, list, purchase and consume assets.

    :param ocean: Ocean object that is being used.
    :type ocean: :class:`.Ocean`
    :param did: Optional did of the Surfer agent

    :param ddo: Optional ddo of the surfer agent, if not provided the agent
        will automatically get the DDO from the network based on the DID.

    :param options: Optional opitions, only `authorization` is used to access the
        Surfer server.

    """
    endPointName = 'metadata-storage'

    def __init__(self, ocean, did=None, ddo=None, options=None):
        """init a standard ocean object"""
        AgentBase.__init__(self, ocean)
        self._did = did
        self._ddo = ddo

        if options is None:
            options = {}

        self._authorization = options.get('authorization')

        if did is None or isinstance(did, str):
            self._did = did
        else:
            raise ValueError('did must be a type string')

        if ddo is None or isinstance(ddo, DDO) or isinstance(ddo, dict):
            self._ddo = ddo
        else:
            raise ValueEror('ddo must be a DOD object or type dict')

        # if DID then try to load in the linked DDO, using squid
        if self._did and not self._ddo:
            model = SquidModel(ocean)
            self._ddo = model.resolve_did_to_ddo(self._did)

    def register_asset(self, asset, account=None ):
        """

        Register an asset with the ocean network (surfer)

        :type asset: :class:`.Asset` object to register
        :param account: This is not used for this agent, so for compatibility it is left in
        :type account: :class:`.Account` object to use for registration.

        :return: A new :class:`.Listing` object that has been registered, if failure then return None.
        :type: :class:`.Listing` class

        For example::

            metadata = json.loads('my_metadata')
            asset = MemoryAsset(metadata)
            agent = SurferAgent(ocean)
            listing = agent.register_asset(asset, account)

            if listing:
                print(f'registered my listing asset for sale with the did {listing.did}')

        """

        # NOTE: use _http_client as per tests/helpers/koi_client.py
        # initialized with https://docs.python.org/3/library/http.client.html
        # and surfer config using http://localhost:8080
        # Consider ocean.registerLocalDID(surferDID,ddoString);
        # as per src/test/java/sg/dex/starfish/samples/SurferConfig.java

        # TODO register asset metadata
        # http://localhost:8080/api-docs/index.html#!/Meta_API/post_api_v1_meta_data
        # curl $args --header 'Content-Type: application/json' \
        #   --header 'Accept: application/json' \
        #   -o "$assetidfile" -d @"$metadatafile" $url/api/v1/meta/data \
        # asset_id = contents of assetidfile without quotes

        # TODO register asset
        # http://localhost:8080/api-docs/index.html#!/Storage_API/post_api_v1_assets_id
        # curl $args --header 'Accept: application/json' \
        #   --form file=@"$asset" $url/api/v1/assets/$assetid ; then
        # WHERE $asset is asset.data, $assetid = asset_id

        model = self._get_surferModel()

        listing = None
        register_data = model.register_asset(asset.metadata)
        if register_data:
            asset_id = register_data['asset_id']
            did = f'{self._did}/{asset_id}'
            asset.set_did(did)
            listing_id=model.create_listing(asset_id)
            listing = Listing(self, did, asset, self._ddo, listing_id)
        return listing

    def validate_asset(self, asset):
        """

        Validate an asset

        :param asset: Asset to validate.
        :return: True if the asset is valid
        """
        pass

    def get_listing(self, did):
        """
        this method is deprecated, as register_asset returns a listing.
        Return an listing on the listing's DID.

        :param str did: DID of the listing, this includes the did of the Surfer Agent Server.

        :return: a registered asset given a DID of the asset
        :type: :class:`.Asset` class

        """
        listing = None
        if SurferAgent.is_did_valid(did):

            data = did_parse(did)

            asset_id = data['path']
            agent_did = 'did:op:' + data['id']
            model = self._get_surferModel(agent_did)
            endpoint = model.get_endpoint('metadata', SurferAgent.endPointName)
            result_data = model.read_asset(asset_id, endpoint)

            if result_data:
                metadata = json.loads(result_data['metadata_text'])
                asset = MemoryAsset(metadata, did)
                listing = Listing(self, did, asset, self._ddo)
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
        pass

    def purchase_asset(self, listing, account):
        """

        Purchase an asset using it's listing and an account.

        :param listing: Listing to use for the purchase.
        :type listing: :class:`.Listing`
        :param account: Ocean account to purchase the asset.
        :type account: :class:`.Account` object to use for registration.

        """
        pass

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
        return False

    def purchase_wait_for_completion(self, purchase_id, timeoutSeconds):
        """

            Wait for completion of the purchase

            TODO: issues here...
            + No method as yet to pass back paramaters and values during the purchase process
            + We assume that the following templates below will always be used.

        """
        pass

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
        return False

    def _get_surferModel(self, did=None, ddo=None, authorization=None):
        """

        Return a new SurferModel object based on the did.
        If did == None then use the loaded did in this class.
        else check to see if the did != self._did, if not then load in the ddo as well
        """

        # if the given did is different, and no ddo, then we are requesting
        # data from a different source, so load in the ddo
        if did and did != self._did and ddo is None:
            if self._did and not self._ddo:
                model = SquidModel(ocean)
                ddo = model.resolve_did_to_ddo(self._did)

        if did is None:
            did = self._did

        if ddo is None:
            ddo = self._ddo

        # TODO: check that the ddo is valid with the did
        if self._authorization is None:
            options = {
                'authorization': authorization
            }
        else:
            options = {
                'authorization': self._authorization
            }

        return SurferModel(self._ocean, did, ddo, options)

    @staticmethod
    def is_did_valid(did):
        """
        Checks to see if the DID string is a valid DID for this type of address for an asset.
        This method only checks the syntax of the DID, it does not resolve the DID
        to see if it is assigned to a valid Asset.

        :param str did: DID string to check to see if it is in a valid format.

        :return: True if the DID is in the format 'did:op:xxxxx/yyyy'
        :type: boolean
        """
        data = did_parse(did)
        return data['path'] and data['id_hex']

    @staticmethod
    def generate_metadata():
        return {"name": "string", "description": "string", "type": "dataset",
                "dateCreated": "2018-11-26T13:27:45.542Z",
                "tags": ["string"],
                "contentType": "string",
                "links": [{"name": "string", "type": "download", "url": "string"}]}
