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

"""

"""
class Ocean():
    """
    .. _Asset class: asset.html
    .. _Config class: config.html

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

    You can provide these parameters in a dictionary or as individual parameters.

    :param filename: Filename of the config file to load.
    :type filename: str or None
    :param contracts_path: path to the contract files ( artifacts ).
    :type contracts_path: str or None
    :param keeper_url: url to the keeper node ( http://localhost:8545 ).
    :type keeper_url: str or None
    :param secret_store_url: url to the secret store node ( http://localhost:12001 ).
    :type secret_store_url: str or None
    :param parity_url: url to the parity node ( http://localhost:8545 ).
    :type parity_url: str or None
    :param aquarius_url: url of the Aquarius metadata service ( http://localhost:5000 ).
    :type aquarius_url: str or None
    :param brizo_url: url of the Brizo consumer service (http://localhost:8030 ).
    :type brizo_url: str or None
    :param storage_path: Path to save temporary storage of assets purchased and consumed ( squid_py.db ).
    :type storage_path: str or None
    :param download_path: Path to save the consumed assets too. ( consume_downloads ).
    :type download_path: str or None
    :param agent_store_did: DID of the agent metadata service.
    :type agent_store_did: str or None
    :param agent_store_auth: Authorziation text to access the metadat service.
    :type agent_store_auth: str or None
    :param gas_limit: The amount of gas you are willing to spend on each block chain transaction ( 30000 ).
    :type gas_limit: int or string

    see the :class:`.Config` class for more details as to the parameters you can pass.

    """

    def __init__(self, *args, **kwargs):
        """
        .. :class: starfish_py.Ocean

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

        :param str agent_service_name: service name of the registration to use to register for the agent.
        :param str endpoint_url: URL of the agents service to register.
        :param object account: Ocean account to use as the owner of the DID->DDO registration.
        :param did: Optional DID of the agent to register, if it already exists
        :type did: str or None

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


        :param dict metadata: metadata dictionary to store for this asset.
        :param object account: Ocean account to use to register this asset.

        :return: A new _Asset_ object that has been registered, if failure then return None.
        :type: :class:`.Asset` class

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

        :param dict metadata: metadata dictonary to store for this asset.

        :return: the asset that has been registered
        :type: :class:`.AssetLight` class

        """

        asset = AssetLight(self)

        # TODO: fix the exit, so that we raise an error or return an asset
        if asset.register(metadata):
            return asset
        return None

    def get_asset(self, did):
        """

        Return an asset based on the asset's DID.

        :param str did: DID of the asset and agent combined.

        :return: a registered asset given a DID of the asset
        :type: :class:`.Asset` class

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

        :param str template_id: Template id of the service level agreement template.
        :param object account: Ocean account to use if this method needs to register the template.

        :return: True if the agreement template has been added, else False if it's already been registered
        :type: boolean

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
        :type: :class:`.Config` class
        """
        return self._config
