"""
    Basic Ocean class to allow for registration and obtaining assets and agents

"""
from web3 import (
    Web3,
    HTTPProvider
)

from squid_py.ocean.ocean import Ocean as SquidOcean
from squid_py.config import Config

from starfish_py.asset.asset import Asset
from starfish_py.asset.asset_light import AssetLight
from starfish_py.config import Config as OceanConfig
from starfish_py.models.squid_model import SquidModel
from starfish_py.agent import Agent


class Ocean():

    def __init__(self, *args, **kwargs):
        """init the basic OceanClient for the connection and contract info"""
        self._config = OceanConfig(*args, **kwargs)

        squid_config = Config(options_dict=self._config.as_squid_dict)
        self._squid_ocean = SquidOcean(squid_config)

        # For development, we use the HTTPProvider Web3 interface
        self._web3 = Web3(HTTPProvider(self._config.keeper_url))

    def register_agent(self, agent_service_name, endpoint_url, account, did=None):
        """
        Register this agent on the block chain
        :param agent_service_name: agent object or name of the registration to use to register an agent
        :param endpoint_url: URL of the agents service to register
        :param account: Ethereum account to use as the owner of the DID->DDO registration
        :param did: DID of the agent to register, if it already exists
        :return private password of the signed DDO
        """

        service_name = None
        if isinstance(agent_service_name, MetadataMarketAgent):
            service_name = agent_service_name.register_name
        elif isinstance(agent_service_name, str):
            service_name = agent_service_name

        if not service_name:
            raise ValueError('Provide an MetadataMarketAgent or a agent service name to register')
        agent = Agent(self)

        return agent.register(service_name, endpoint_url, account, did)



    def register_asset(self, metadata, account):
        """
        Register an on chain asset
        :param metadata: dict of the metadata
        :return The new asset registered, or return None on error
        """

        asset = Asset(self)

        # TODO: fix the exit, so that we raise an error or return an asset
        if asset.register(metadata, account):
            return asset
        return None

    def register_asset_light(self, metadata):
        """
        Register an asset on the off chain system using an metadata storage agent
        :return: the asset that has been registered
        """

        asset = AssetLight(self)

        # TODO: fix the exit, so that we raise an error or return an asset
        if asset.register(metadata):
            return asset
        return None

    def get_asset(self, did):
        """
        :param: did: DID of the asset and agent combined.
        :return a registered asset given a DID of the asset
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
        :return: True if the agreemtn template gets added, else False if it's already
        registered
        """
        model = SquidModel(self)
        if not model.is_service_agreement_template_registered(template_id):
            model.register_service_agreement_template(template_id, account)
            return True
        return False

    @property
    def accounts(self):
        """return the ethereum accounts"""
        return self._squid_ocean.get_accounts()

    @property
    def web3(self):
        """return the web3 instance"""
        return self._web3

    @property
    def keeper(self):
        """return the keeper contracts"""
        return self._squid_ocean.keeper

    @property
    def squid(self):
        """return squid ocean library"""
        return self._squid_ocean

    @property
    def config(self):
        """return config info"""
        return self._config