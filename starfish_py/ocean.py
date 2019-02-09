"""

Ocean class to access the Ocean eco system.

"""
from web3 import (
    Web3,
    HTTPProvider
)

from squid_py.ocean.ocean import Ocean as SquidOcean
from squid_py.config import Config

from starfish_py import Asset
from starfish_py import AssetLight
from starfish_py import Config as OceanConfig
from starfish_py.models.squid_model import SquidModel
from starfish_py import Agent


class Ocean():
    """

    The Ocean class connects to the ocean network.

    For example to use this class you can do the following::

        from starfish_py.ocean import Ocean

        my_config = {
            'contracts_path': 'artifacts',
            'keeper_url': 'http://localhost:8545',
            'secret_store_url': 'http://localhost:12001',
            'parity_url': 'http://localhost:8545',
        }
        ocean = Ocean(my_config)

    :param contracts_path: path to the contract files ( artifacts ).
    :param keeper_url: url to the keeper node ( http://localhost:8545 ).
    :param secret_store_url: url to the secret store node ( http://localhost:12001 ).
    :param parity_url: url to the parity node ( 'http://localhost:8545 ).

    see the :func:`starfish_py.config` module for more details.
    """

    def __init__(self, *args, **kwargs):
        """

        init the basic Ocean class for the connection and contract info


        """
        self._config = OceanConfig(*args, **kwargs)

        squid_config = Config(options_dict=self._config.as_squid_dict)
        self._squid_ocean = SquidOcean(squid_config)

        # For development, we use the HTTPProvider Web3 interface
        self.__web3 = Web3(HTTPProvider(self._config.keeper_url))

    def register_agent(self, agent_service_name, endpoint_url, account, did=None):
        """

        Register this agent on the block chain.

        :param agent_service_name: service name of the registration to use to register for the agent.
        :param endpoint_url: URL of the agents service to register.
        :param account: Ocean account to use as the owner of the DID->DDO registration.
        :param did: DID of the agent to register, if it already exists

        :return: a list of DID, DDO and  private pem of the registered DDO.
        :type: string

        For example::

            # register the public surfer on the block chain
            did, ddo, key_pem = ocean.register_agent('surfer', 'https://market_surfer.io', ocean.accounts[0])

        """

        agent = Agent(self)
        return agent.register(agent_service_name, endpoint_url, account, did)



    def register_asset(self, metadata, account):
        """

        Register an asset with the ocean network.


        :param metadata: metadata dictionary to store for this asset.
        :param account: Ocean account to use to register this asset.

        :return: A new _Asset_ object that has been registered, if failure then return None.

        For example::

            metadata = json.loads('my_metadata')
            account = ocean.accounts[0]
            asset = ocean.register_asset(metadata, account)
            if asset:
                print(f'registered my asset with the did {asset.did}')

        """

        asset = Asset(self)

        # TODO: fix the exit, so that we raise an error or return an asset
        if asset.register(metadata, account):
            return asset
        return None

    def register_asset_light(self, metadata):
        """

        Register an asset using the **off chain** system using an metadata storage agent

        :param metadata: metadata dictonary to store for this asset.

        :return: the asset that has been registered

        """

        asset = AssetLight(self)

        # TODO: fix the exit, so that we raise an error or return an asset
        if asset.register(metadata):
            return asset
        return None

    def get_asset(self, did):
        """

        Return an asset based on the asset's DID.

        :param did: DID of the asset and agent combined.

        :return: a registered asset given a DID of the asset
        """
        asset = None
        if Asset.is_did_valid(did):
            asset = Asset(self, did)
        elif AssetLight.is_did_valid(did):
            asset = AssetLight(self, did)
        else:
            raise ValueError(f'Invalid did "{did}" for an asset')

        if not asset.is_empty:
            if asset.read():
                return asset
        return None


    def search_registered_assets(self, text, sort=None, offset=100, page=0):
        """

        Search the off chain storage for an asset with the givien 'text'

        :param text: Test to search all metadata items for.
        :param sort: sort the results ( defaults: None, no sort).
        :param offset: Return the result from with the maximum record count ( defaults: 100 ).
        :param page: Returns the page number based on the offset.

        :return: a list of assets objects found using the search.

        For example::

            # return the 300 -> 399 records in the search for the text 'weather' in the metadata.
            my_result = ocean.search_registered_assets('weather', None, 100, 3)

        """
        asset_list = None
        model = SquidModel(self)
        ddo_list = model.search_assets(text, sort, offset, page)
        if ddo_list:
            asset_list = []
            for ddo in ddo_list:
                asset = Asset(self, ddo = ddo)
                asset_list.append(asset)
        return asset_list

    def register_service_level_agreement_template(self, template_id, account):
        """

        Register the service level agreement on the block chain.

        This is currently only **used for testing**, as we assume that Ocean has
        already registered a service level agreement template onchain for usage.

        :param template_id: Template id of the service level agreement template.
        :param account: Ocean account to use if this method needs to register the template.

        :return: True if the agreement template has been added, else False if it's already been registered

        """
        model = SquidModel(self)
        if not model.is_service_agreement_template_registered(template_id):
            model.register_service_agreement_template(template_id, account)
            return True
        return False


    @property
    def accounts(self):
        """
        :return: a list of ocean accounts
        :type: list of accounts

        """
        return self._squid_ocean.get_accounts()

    @property
    def _web3(self):
        """return the web3 instance"""
        return self.__web3

    @property
    def _keeper(self):
        """return the keeper contracts"""
        return self._squid_ocean.keeper

    @property
    def _squid(self):
        """return squid ocean library"""
        return self._squid_ocean

    @property
    def config(self):
        """

        :return: the used config object for this connection
        :type: :func:`starfish_py.config` object

        """
        return self._config
