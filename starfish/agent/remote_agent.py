"""

Surfer Agent class to provide basic functionality for Ocean Agents

In starfish-java, this is named as `RemoteAgent`

"""
import logging
import time
from urllib.parse import urljoin


from eth_utils import remove_0x_prefix

from starfish.agent import AgentBase
from starfish.agent.services import Services
from starfish.asset import (
    DataAsset,
    OperationAsset,
    create_asset_from_metadata_text,
    is_asset_hash_valid
)
from starfish.ddo.ddo import DDO
from starfish.exceptions import (
    StarfishAssetInvalid,
    StarfishRemoteAgentInvalidAccess
)
from starfish.job import Job
from starfish.listing import Listing
from starfish.middleware.remote_agent_adapter import RemoteAgentAdapter
from starfish.utils.did import (
    decode_to_asset_id,
    did_generate_random,
    did_parse,
    is_did
)

SUPPORTED_SERVICES = {
    'meta': 'DEP.Meta.v1',
    'storage': 'DEP.Storage.v1',
    'invoke': 'DEP.Invoke.v1',
    'market': 'DEP.Market.v1',
    'trust': 'DEP.Trust.v1',
    'auth': 'DEP.Auth.v1',
}


logger = logging.getLogger(__name__)


class RemoteAgent(AgentBase):
    """

    Remote Agent class allows to register, list, purchase and consume assets.

    :param ocean: Ocean object that is being used.
    :type ocean: :class:`.Ocean`
    :param did: Optional did of the Surfer agent

    :param ddo: Optional ddo of the remote agent, if not provided the agent
        will automatically get the DDO from the network based on the DID.

    :param dict authentication: authentication is a dict of values to allow for authentication access to
        a remote agent.
        Currently the following values are supported:

            username
            password
            token

    """
    service_types = SUPPORTED_SERVICES

    def __init__(self, network, ddo, authentication=None):
        self._authentication = authentication

        if isinstance(ddo, dict):
            ddo = DDO(dictionary=ddo)
        elif isinstance(ddo, str):
            ddo = DDO(json_text=ddo)
        elif isinstance(ddo, DDO):
            pass
        else:
            raise ValueError(f'Unknown ddo type {ddo}')
        AgentBase.__init__(self, network, ddo)

        self._adapter = RemoteAgentAdapter()

    @staticmethod
    def load(network, asset_agent_did_url, authentication=None):
        ddo_text = None

        if is_did(asset_agent_did_url):
            ddo_text = RemoteAgent.resolve_network_ddo(network, asset_agent_did_url)
        if ddo_text is None:
            ddo_text = RemoteAgent.resolve_url_ddo(asset_agent_did_url, authentication)

        if ddo_text:
            return RemoteAgent(network, ddo_text, authentication)

        return None

    @staticmethod
    def register(network, register_account, ddo, authentication=None):
        network.register_did(register_account, ddo.did, ddo.as_text())
        return RemoteAgent(network, ddo.as_text(), authentication)

    def register_asset(self, asset):
        """

        Register an asset with Surfer

        :param asset: asset object to register
        :type asset: :class:`.DataAsset` object to register
        :param account: This is not used for this agent, so for compatibility it is left in
        :type account: :class:`.Account` object to use for registration.

        :return: A :class:`.AssetBase` object that has been registered, if failure then return None.
        :type: :class:`.AssetBase` class

        For example::

            asset = DataAsset.create('test data asset', 'Some test data')
            listing_data = { 'price': 3.457, 'description': 'my data is for sale' }
            agent = SurferAgent(network, ddo)
            asset = agent.register_asset(asset, account)
            print(f'Asset DID is {asset.did}')

        """

        if self._ddo is None:
            raise ValueError('The agent must have a valid ddo')

        url = self.get_endpoint('meta')
        authorization_token = self.get_authorization_token()
        register_data = self._adapter.register_asset(asset.metadata_text, url, authorization_token)
        if register_data:
            asset_id = register_data['asset_id']
            did = f'{self._ddo.did}/{asset_id}'
            asset.set_did(did)
        return asset

    def create_listing(self, listing_data, asset_did):
        """

        Create a listing on the market place for this asset

        :param dict listing_data:  Listing inforamiton to give for this asset
        :param str asset_did: asset DID to assign to this listing
        :return: A new :class:`.Listing` object that has been registered, if failure then return None.
        :type: :class:`.Listing` class

        For example::

            asset = DataAsset.create('test data asset', 'Some test data')
            agent = SurferAgent(network)
            asset = agent.register_asset(asset, account)

            listing_data = { 'price': 3.457, 'description': 'my data is for sale' }
            listing = agent.create_listing(listing_data, asset)
            if listing:
                print(f'registered my listing asset for sale with the did {listing.did}')


        """

        if not isinstance(listing_data, dict):
            raise ValueError('You must provide a dict as the listing data')

        url = self.get_endpoint('market')
        authorization_token = self.get_authorization_token()

        asset_id = decode_to_asset_id(asset_did)
        data = self._adapter.create_listing(listing_data, asset_id, url, authorization_token)
        listing = Listing(self, data['id'], asset_did, data)
        return listing

    def update_listing(self, listing):
        """

        Update the listing to the agent server.

        :param listing: Listing object to update
        :type listing: :class:`.Listing` class

        """
        url = self.get_endpoint('market')
        authorization_token = self.get_authorization_token()

        return self._adapter.update_listing(listing.listing_id, listing.data, url, authorization_token)

    def validate_asset(self, asset):
        """

        Validate an asset

        :param asset: Asset to validate.
        :return: True if the asset is valid
        """
        pass

    def upload_asset(self, asset):

        if not isinstance(asset, DataAsset):
            raise TypeError('Only DataAsset is supported')

        if not asset.data:
            raise ValueError('No data to upload')

        url = self.get_endpoint('storage')
        authorization_token = self.get_authorization_token()
        asset_id = remove_0x_prefix(asset.asset_id)

        return self._adapter.upload_asset_data(asset_id, asset.data, url, authorization_token)

    def download_asset(self, asset_did_id):
        """
        Download an asset

        :param str asset_did_id: Asset id or asset did to download

        :return: an Asset
        :type: :class:`.DataAsset` class

        """

        url = self.get_endpoint('storage')
        authorization_token = self.get_authorization_token()

        asset_id = decode_to_asset_id(asset_did_id)
        if not asset_id:
            raise ValueError(f'{asset_did_id} is not an asset id or asset did')

        data = self._adapter.download_asset(asset_id, url, authorization_token)
        store_asset = self.get_asset(asset_id)
        asset = DataAsset(
            store_asset.metadata,
            store_asset.did,
            data=data,
            metadata_text=store_asset.metadata_text
        )
        return asset

    def get_listing(self, listing_id):
        """
        Return an listing on the listings id.

        :param str listing_id: Id of the listing.

        :return: a listing object
        :type: :class:`.Asset` class

        """
        listing = None
        url = self.get_endpoint('market')
        authorization_token = self.get_authorization_token()

        data = self._adapter.get_listing(listing_id, url, authorization_token)
        if data:
            asset_id = data['assetid']
            url = self.get_endpoint('meta')
            read_metadata = self._adapter.read_metadata(asset_id, url, authorization_token)
            if read_metadata:
                asset = self._create_asset_from_read(asset_id, read_metadata)
                listing = Listing(self, data['id'], asset, data)
        return listing

    def get_asset(self, asset_did_id):
        """

        This is for compatability for Surfer calls to get an asset directly from Surfer

        :param str asset_did_id: Asset DID or asset Id of the asset to read or did/asset_id

        :return: an asset class
        :type: :class:`.AssetBase` class

        """
        asset = None
        asset_id = decode_to_asset_id(asset_did_id)
        url = self.get_endpoint('meta')
        authorization_token = self.get_authorization_token()
        read_metadata = self._adapter.read_metadata(asset_id, url, authorization_token)
        if read_metadata:
            asset = self._create_asset_from_read(asset_id, read_metadata)
        return asset

    def get_listings(self):
        """
        Returns all listings

        :return: List of listing objects

        """
        listings = []
        url = self.get_endpoint('market')
        authorization_token = self.get_authorization_token()
        listings_data = self._adapter.get_listings(url, authorization_token)
        if listings_data:
            for data in listings_data:
                asset_id = data['assetid']
                url = self.get_endpoint('meta')
                read_metadata = self._adapter.read_metadata(asset_id, url, authorization_token)
                if read_metadata:
                    asset = self._create_asset_from_read(asset_id, read_metadata)
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
        url = self.get_endpoint('invoke', 'jobs')
        authorization_token = self.get_authorization_token()
        data = self._adapter.get_job(job_id, url, authorization_token)
        if data:
            status = data.get('status', None)
            outputs = data.get('outputs', None)
            job = Job(job_id, status, outputs)
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
        # TODO: implement search listing in remote
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
        purchase = {'listingid': listing.listing_id}
        if purchase_id:
            purchase['id'] = purchase_id
        if status:
            purchase['status'] = status
        if info:
            purchase['info'] = info
        if agreement:
            purchase['agreement'] = agreement
        url = self.get_endpoint('market')
        authorization_token = self.get_authorization_token()
        return self._adapter.purchase_asset(purchase, url, authorization_token)

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

    def invoke(self, asset, inputs=None, is_async=False):
        """

        Call an operation asset with inputs to execute a remote call.

        :param asset: Operation asset to use for this invoke call
        :type asset: :class:`.OperationAsset`
        :param dict inputs: Inputs to send to the invoke call

        :return: Return a dict of the result.
        :type: dict


        """
        if not isinstance(asset, OperationAsset):
            raise ValueError('Asset is not a OperationAsset')

        mode_type = 'async' if is_async else 'sync'
        if not asset.is_mode(mode_type):
            raise TypeError(f'This operation asset does not support {mode_type}')
        if not inputs:
            inputs = {}

        url = self.get_endpoint('invoke', mode_type)
        authorization_token = self.get_authorization_token()
        response = self._adapter.invoke(remove_0x_prefix(asset.asset_id), inputs, url, authorization_token)
        return response

    def get_authorization_token(self):

        if self._authentication and 'token' in self._authentication:
            if self._authentication['token']:
                return self._authentication['token']

        url = self.get_endpoint('auth', 'token')
        token = None
        if url and self._authentication and 'username' in self._authentication:
            token = self._adapter.get_authorization_token(
                self._authentication['username'],
                self._authentication.get('password', ''),
                url
            )
            if token is None:
                raise StarfishRemoteAgentInvalidAccess(f'Unable to obtain a token from {url}')

        return token

    def get_metadata_list(self):
        url = self.get_endpoint('meta')
        authorization_token = self.get_authorization_token()
        return self._adapter.get_metadata_list(url, authorization_token)

    @property
    def ddo(self):
        """

        Return the registered DDO for this agent

        :return: DDO registered for this agent
        :type: :class:`.DDO`
        """
        return self._ddo

    @staticmethod
    def is_did_valid(did):
        """
        Checks to see if the DID string is a valid DID for this type of address for an asset.
        This method only checks the syntax of the DID, it does not resolve the DID
        to see if it is assigned to a valid Asset.

        :param str did: DID string to check to see if it is in a valid format.

        :return: True if the DID is in the format 'did:dep:xxxxx/yyyy'
        :type: boolean
        """
        data = did_parse(did)
        return data['path'] and data['id_hex']

    @staticmethod
    def generate_ddo(base_url_or_services, service_list=None, is_add_proof=False):
        """
        Generate a DDO for the remote agent url. This DDO will contain the supported
        endpoints for the remote agent

        :param str base_url_or_services: Base URL of the remote agent
        :param dict base_url_or_services: Service dict to use. This has to be in the sample format:
            see starfish.agent.services SERVICES

        :param :class:`agent.services.Services` base_url_or_services: An agent Services object.

        :param dict service_list: Optional list of services to regsiter. This is only if the
            base_url_or_services is a string containing the base_url.

        :return: created DDO object assigned to the url of the remote agent service
        :type: :class:.`DDO`

            generate_ddo('http://localhost', ['metadata', 'storage'])

            # is the same as
            services = Services('http://localhost', service_list=['metadata', 'storage'])
            generate_ddo(services)

            # or

            generate_ddo(services.as_dict)

        """

        service_items = None

        if isinstance(base_url_or_services, str):
            services = Services(base_url_or_services, service_list)
            service_items = services.as_dict
        elif isinstance(base_url_or_services, dict):
            service_items = base_url_or_services
        elif isinstance(base_url_or_services, Services):
            service_items = base_url_or_services.as_dict
        else:
            raise(TypeError('Invalid services type, must be a string, dict or Services object'))

        did = did_generate_random()
        ddo = DDO(did)
        for _service_name, service_item in service_items.items():
            ddo.add_service(service_item['type'], service_item['url'], None)

        if is_add_proof:
            # add a signature
            private_key_pem = ddo.add_signature()
            # add the static proof
            ddo.add_proof(0, private_key_pem)

        return ddo

    def _create_asset_from_read(self, asset_id, read_metadata):
        # check the hash of the reading asset
        asset_id = remove_0x_prefix(asset_id)
        if not is_asset_hash_valid(asset_id, read_metadata['hash']):
            raise StarfishAssetInvalid(f' asset {asset_id} is not valid')

        did = f'{self._ddo.did}/{asset_id}'
        metadata_text = read_metadata['metadata_text']
        asset = create_asset_from_metadata_text(metadata_text, did)
        return asset

    def get_endpoint(self, name, uri=None):
        """return the endpoint based on the name of the service or service type"""
        service_type = RemoteAgent.find_supported_service_type(name)
        if service_type is None:
            message = f'unknown surfer endpoint service name or type: {name}'
            logger.error(message)
            raise ValueError(message)

        endpoint = None
        if self._ddo:
            service = self._ddo.get_service(service_type)
            if not service:
                message = f'unable to find surfer endpoint service type {service_type}'
                logger.error(message)
                raise ValueError(message)
            endpoint = service.endpoint
        if not endpoint:
            message = f'unable to find surfer endpoint for {name} = {service_type}'
            logger.error(message)
            raise ValueError(message)
        if uri:
            endpoint = urljoin(endpoint + '/', uri)
        return endpoint

    @staticmethod
    def find_supported_service_type(search_name_type):
        """ return the supported service record if the name or service type is found
        else return None """
        for name, service_type in SUPPORTED_SERVICES.items():
            if service_type == search_name_type:
                return service_type
            if name == search_name_type:
                return service_type
        return None

    @staticmethod
    def resolve_network_ddo(network, did):
        """

        Resolves the remote agent via the dnetwork using it's did to get the agent DDO

        :param object network: DNetwork to resolve the did
        :param str did: DID of the remote agent to resolve and get DDO
        :return dict: DDO or None if not found in the network

        """
        if did:
            return network.resolve_did(did)

    @staticmethod
    def resolve_url_ddo(url, authentication=None):
        """

        Resolves the remote agent ddo using the url of the agent

        :param str url: url of the remote agent
        :param str username: optional username for access to the remote agent
        :param str password: optional password for access to the remote agent
        :return dict: DDO or None if not found
        """

        ddo = None
        if url:
            adapter = RemoteAgentAdapter()
            token = None
            token_url = urljoin(f'{url}/', 'api/v1/auth/token')
            if authentication and 'username' in authentication:
                token = adapter.get_authorization_token(
                    authentication['username'],
                    authentication.get('password', ''),
                    token_url
                )

            ddo = adapter.get_ddo(url, token)
        return ddo
