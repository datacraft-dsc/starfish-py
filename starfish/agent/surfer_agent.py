"""

Surfer Agent class to provide basic functionality for Ocean Agents

In starfish-java, this is named as `RemoteAgent`

"""
import secrets
import re
import json
import time

from eth_utils import remove_0x_prefix

from starfish.account import Account
from starfish.agent import AgentBase
from starfish.asset import (
    MemoryAsset,
    OperationAsset,
    FileAsset,
    create_asset_from_metadata,
)
from starfish.models.surfer_model import SurferModel, SUPPORTED_SERVICES
from starfish.models.squid_model import SquidModel
from starfish.utils.did import did_parse
from starfish.listing import Listing
from starfish.job import Job
from starfish.ddo.starfish_ddo import StarfishDDO




from squid_py.ddo.ddo import DDO

class SurferAgent(AgentBase):
    """

    Surfer Agent class allows to register, list, purchase and consume assets.

    :param ocean: Ocean object that is being used.
    :type ocean: :class:`.Ocean`
    :param did: Optional did of the Surfer agent

    :param ddo: Optional ddo of the surfer agent, if not provided the agent
        will automatically get the DDO from the network based on the DID.

    :param options: Optional options, only `authorization` is used to access the
        Surfer server.

    """
    services = SUPPORTED_SERVICES


    def __init__(self, ocean, did=None, ddo=None, options=None):
        """init a standard ocean object"""
        AgentBase.__init__(self, ocean)
        self._did = None
        self._ddo = None

        if options is None:
            options = {}

        # set the DID
        if did is None or isinstance(did, str):
            self._did = did
        else:
            raise ValueError('did must be a string or None')

        # set the DDO
        if isinstance(ddo, dict):
            self._ddo = StarfishDDO(dictionary=ddo)
        elif isinstance(ddo, str):
            self._ddo = StarfishDDO(json_text=ddo)
        elif isinstance(ddo, StarfishDDO):
            self._ddo = ddo
        elif ddo is None:
            if self._did:
                self._ddo = self._resolve_ddo_from_did(self._did)
        else:
            raise ValueError('ddo can be one of the following: None, StarfishDDO object or type dict')

        # incase the user just sends a ddo without a did
        if self._did is None and self._ddo:
            self._did = self._ddo.did


        # if DID and no DDO then try to load in the registered DDO, using squid
        if self._did and not self._ddo:
            model = SquidModel(ocean)
            ddo_text = model.resolve_did_to_ddo(self._did)
            if not ddo_text:
                raise ValueError(f'cannot find registered agent at {did}')
            self._ddo = StarfishDDO(json_text=ddo_text)

        if self._did is None and self._ddo:
            self._did = self._ddo.did

        self._authorization = options.get('authorization')
        if self._authorization is None and 'url' in options and 'username' in options:
            # if no authorization, then we may need to create one
            self._authorization = SurferModel.get_authorization_token(
                options['url'],
                options['username'],
                options.get('password', '')
            )

    def register_asset(self, asset, listing_data, account=None ):
        """

        Register an asset with the ocean network (surfer)

        :param asset: asset object to register
        :type asset: :class:`.Asset` object to register
        :param dict listing_data:  Listing inforamiton to give for this asset
        :param account: This is not used for this agent, so for compatibility it is left in
        :type account: :class:`.Account` object to use for registration.

        :return: A new :class:`.Listing` object that has been registered, if failure then return None.
        :type: :class:`.Listing` class

        For example::

            asset = MemoryAsset(data='Some test data')
            listing_data = { 'price': 3.457, 'description': 'my data is for sale' }
            agent = SurferAgent(ocean)
            listing = agent.register_asset(asset,listing_data, account)

            if listing:
                print(f'registered my listing asset for sale with the did {listing.did}')

        """
        model = self._get_surferModel()

        if self._did is None:
            raise ValueError('The agent must have a valid did')

        if not isinstance(listing_data, dict):
            raise ValueError('You must provide a dict as the listing data')

        listing = None

        register_data = model.register_asset(asset.metadata)
        if register_data:
            asset_id = register_data['asset_id']
            did = f'{self._did}/{asset_id}'
            asset.set_did(did)
            data = model.create_listing(asset_id, listing_data)
            listing = Listing(self, data['id'], asset, data)
        return listing

    def validate_asset(self, asset):
        """

        Validate an asset

        :param asset: Asset to validate.
        :return: True if the asset is valid
        """
        pass

    def upload_asset(self, asset):

        if not (isinstance(asset, MemoryAsset) or isinstance(asset, FileAsset)):
            raise TypeError('Only MemoryAsset or FileAsset are supported')
        if not asset.data:
            raise ValueError('No data to upload')

        model = self._get_surferModel()
        url = self.get_asset_store_url(asset.asset_id)
        return model.upload_asset_data(url, asset.asset_id, asset.data)


    def download_asset(self, asset_id, url):
        """
        Download an asset

        :param str url: url of the asset_id.

        :return: an Asset
        :type: :class:`.MemoryAsset` class

        """
        model = self._get_surferModel()
        data = model.download_asset(url)
        store_asset = self.get_asset(asset_id)
        asset = MemoryAsset(store_asset.metadata, store_asset.did, data=data)
        return asset

    def get_asset_store_url(self, asset_id):
        model = self._get_surferModel()
        return model.get_asset_store_url(remove_0x_prefix(asset_id))

    def get_listing(self, listing_id):
        """
        Return an listing on the listings id.

        :param str listing_id: Id of the listing.

        :return: a listing object
        :type: :class:`.Asset` class

        """
        model = self._get_surferModel()
        listing = None
        data = model.get_listing(listing_id)
        if data:
            asset_id = data['assetid']
            read_metadata = model.read_metadata(asset_id)
            if read_metadata:
                metadata = json.loads(read_metadata['metadata_text'])
                did = f'{self._did}/{asset_id}'
                asset = create_asset_from_metadata(metadata, did)
                listing = Listing(self, data['id'], asset, data)
        return listing

    def get_asset(self, asset_id):
        """

        This is for compatability for Surfer calls to get an asset directly from Surfer

        :param str asset_id: Id of the asset to read

        :return: an asset class
        :type: :class:`.AssetBase` class

        """
        asset = None
        model = self._get_surferModel()
        clean_asset_id = remove_0x_prefix(asset_id)
        read_metadata = model.read_metadata(clean_asset_id)
        if read_metadata:
            metadata = json.loads(read_metadata['metadata_text'])
            did = f'{self._did}/{clean_asset_id}'
            asset = create_asset_from_metadata(metadata, did)
        return asset

    def get_listings(self):
        """
        Returns all listings

        :return: List of listing objects

        """
        model = self._get_surferModel()
        listings = []
        listings_data = model.get_listings()
        if listings_data:
            for data in listings_data:
                asset_id = data['assetid']
                read_metadata = model.read_metadata(asset_id)
                if read_metadata:
                    metadata = json.loads(read_metadata['metadata_text'])
                    did = f'{self._did}/{asset_id}'
                    asset = MemoryAsset(metadata, did)
                    listing = Listing(self, data['id'], asset, data)
                    listings.append(listing)
        return listings

    def get_job(self, job_id):
        """

        Get a job from the invoke service ( koi )

        :param str job_id: Id of the job to get

        :return: a job class
        :type: :class:`starfish.job.Job` class

        """
        job = None
        model = self._get_surferModel()
        data = model.get_job(job_id)
        if data:
            status = data.get('status', None)
            results = data.get('results', None)
            job = Job(job_id, status, results)
        return job

    def job_wait_for_completion(self, job_id, timeout_seconds=60, sleep_seconds=1):
        """

        Wait for a job to complete, with optional timeout seconds.

        :param int job_id: Job id to wait for completion
        :param int timeout_seconds: optional time in seconds to wait for job to complete, defaults to 60 seconds
        :param int sleep_seconds: optional number of seconds to sleep between polling the job status, == 0 no sleeping

        :return: Job object if finished, else False for timed out
        :type: :class:`starfish.job.Job` class or False

        """
        timeout_time = time.time() + timeout_seconds
        while timeout_time > time.time():
            job = self.get_job(job_id)
            if job.is_finished:
                return job
            if sleep_seconds > 0:
                time.sleep(sleep_seconds)
        return False

    def update_listing(self, listing):
        """

        Update the listing to the agent server.

        :param listing: Listing object to update
        :type listing: :class:`.Listing` class

        """
        model = self._get_surferModel()
        return model.update_listing(listing.listing_id, listing.data)

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
        # TODO: implement search listing in surfer
        pass

    def purchase_asset(self, listing, account, purchase_id=None, status=None,
                       info=None, agreement=None):
        """

        Purchase an asset using it's listing and an account.

        :param listing: Listing to use for the purchase.
        :type listing: :class:`.Listing`
        :param account: Ocean account to purchase the asset.
        :type account: :class:`.Account` object to use for registration.
        :param purchase_id: purchase id (optional)
        :type purchase_id: str or None
        :param status: purchase status (optional)
        :type status: str or None
        :param info: purchase info (optional)
        :type info: dict or None
        :param agreement: purchase agreement (optional)
        :type agreement: dict or None

        """
        model = self._get_surferModel()
        purchase = {'listingid': listing.listing_id}
        if purchase_id:
            purchase['id'] = purchase_id
        if status:
            purchase['status'] = status
        if info:
            purchase['info'] = info
        if agreement:
            purchase['agreement'] = agreement
        return model.purchase_asset(purchase)

    def is_access_granted_for_asset(self, asset, account, purchase_id=None):
        """

        Check to see if the account and purchase_id have access to the assed data.


        :param asset: Asset to check for access.
        :type asset: :class:`.Asset` object
        :param account: Ocean account to purchase the asset.
        :type account: :class:`.Account` object to use for registration.
        :param str purchase_id: purchase id that was used to purchase the asset.

        :return: True if the asset can be accessed and consumed.
        :type: boolean
        """
        return False

    def get_asset_purchase_ids(self, asset):
        """

        Returns as list of purchase id's that have been used for this asset

        :param asset: Asset to return purchase details.
        :type asset: :class:`.Asset` object

        :return: list of purchase ids
        :type: list

        """
        return []

    def purchase_wait_for_completion(self, asset, account, purchase_id, timeoutSeconds):
        """

            Wait for completion of the purchase

            TODO: issues here...
            + No method as yet to pass back paramaters and values during the purchase process
            + We assume that the following templates below will always be used.

        """
        pass

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

        :return: True if the asset has been consumed and downloaded
        :type: boolean

        """
        return False

    def invoke_result(self, asset, params=None, is_async=False):
        """

        Call an operation asset with params to execute a remote call.

        :param asset: Operation asset to use for this invoke call
        :type asset: :class:`.OperationAsset`
        :param dict params: Parameters to send to the invoke call

        :return: Return a dict of the result.
        :type: dict


        """

        if not isinstance(asset, OperationAsset):
            raise ValueError('Asset is not a OperationAsset')

        mode_type = 'async' if is_async else 'sync'
        if not asset.is_mode(mode_type):
            raise TypeError(f'This operation asset does not support {mode_type}')
        if not params:
            params = {}
        model = self._get_surferModel()
        response = model.invoke(remove_0x_prefix(asset.asset_id), params, is_async)
        return response

    def get_endpoint(self, name):
        """

        Return the endpoint of the service available for this agent
        :param str name: name or type of the service, e.g. 'metadata', 'storage', 'Ocean.Meta.v1'
        """
        model = self._get_surferModel()
        supported_service = SurferModel.find_supported_service(name)
        if supported_service is None:
            raise ValueError(f'This agent does not support the following service name or type {name}')
        return model.get_endpoint(name)


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

    def _resolve_ddo_from_did(self, did):
        model = SquidModel(self._ocean)
        ddo_text = model.resolve_did(self._did)
        if not ddo_text:
            raise ValueError(f'cannot find registered agent at {did}')
        return StarfishDDO(json_text=ddo_text)

    @property
    def did(self):
        """

        Return the did for this surfer agent.

        :return: did of the registered agent
        :type: string
        """
        return self._did
    @property
    def ddo(self):
        """

        Return the registered DDO for this agent

        :return: DDO registered for this agent
        :type: :class:`.StarfishDDO`
        """
        return self._ddo

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
    def decode_asset_did(did):
        data = did_parse(did)
        return data['id'], data['path']

    @staticmethod
    def generate_ddo(url, services=None):
        """
        Generate a DDO for the surfer url. This DDO will contain the supported
        endpoints for the surfer

        :param str url: URL of the remote surfer agent
        :param dict services: Optional dict of services urls that are not assigned to the main url.

        :return: created DDO object assigned to the url of the remote surfer agent service
        :type: :class:.`DDO`
        """

        did = SquidModel.generate_did()
        service_endpoints = SurferModel.generate_service_endpoints(url)
        ddo = StarfishDDO(did)
        for service_endpoint in service_endpoints:
            service_name = service_endpoint['name']
            url = service_endpoint['url']
            if services and service_name in services:
                url = services[service_name]
            ddo.add_service(service_endpoint['type'], url, None)

        # add a signature
        private_key_pem = ddo.add_signature()
        # add the static proof
        ddo.add_proof(0, private_key_pem)

        return ddo

    @staticmethod
    def generate_metadata():
        return {"name": "string", "description": "string", "type": "dataset",
                "dateCreated": "2018-11-26T13:27:45.542Z",
                "tags": ["string"],
                "contentType": "string",
                "links": [{"name": "string", "type": "download", "url": "string"}]}
