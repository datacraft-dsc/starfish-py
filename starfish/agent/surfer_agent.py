"""

Surfer Agent class to provide basic functionality for Ocean Agents

In starfish-java, this is named as `RemoteAgent`

"""

import secrets
import re
import json

# from squid_py.did import id_to_did

from starfish.account import Account
from starfish.agent import Agent
from starfish.asset import MemoryAsset
from starfish.models.surfer_model import SurferModel
from starfish.models.squid_model import SquidModel
from starfish.asset import Asset
from starfish.utils.did import did_parse
from starfish.listing import Listing



from squid_py.ddo.ddo import DDO

class SurferAgent(Agent):
    """

    Surfer Agent class allows to register, list, purchase and consume assets.

    :param ocean: Ocean object that is being used.
    :type ocean: :class:`.Ocean`

    """
    endPointName = 'metadata-storage'

    def __init__(self, ocean, did=None, ddo=None, options=None):
        """init a standard ocean object"""
        Agent.__init__(self, ocean)
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


    def register_asset(self, asset, account=None):
        """

        Register a memory asset with the ocean network (surfer)
        FIXME BELOW

        :type asset: :class:`.Asset` object to register
        :param account: Ocean account to use to register this asset.
        :type account: :class:`.Account` object to use for registration.

        :return: A new :class:`.Listing` object that has been registered, if failure then return None.
        :type: :class:`.Listing` class

        For example::

            metadata = json.loads('my_metadata')
            # get your publisher account
            account = ocean.get_account('0x00bd138abd70e2f00903268f3db08f2d25677c9e')
            agent = SurferAgent(ocean)
            listing = agent.register_asset(metadata, account)

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
        endpoint = model.get_endpoint('metadata', SurferAgent.endPointName)
        register_data = model.register_asset(asset.metadata, endpoint)
        if register_data:
            asset_id = register_data['asset_id']
            did = f'{self._did}/{asset_id}'
            asset.set_did(did)
            listing = Listing(self, did, asset, self._ddo)
        return listing



    def get_listing(self, did):
        """

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

        options = {
            'authorization': authorization
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
