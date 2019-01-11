"""
    Basic Ocean class to allow for registration and obtaining assets and agents

"""
from web3 import (
    Web3,
    HTTPProvider
)

from ocean_py.asset.asset_on_chain import AssetOnChain
from ocean_py.asset.asset_off_chain import AssetOffChain
from ocean_py.config import Config as OceanConfig
from ocean_py.agents.metadata_agent import MetadataAgent

from squid_py.ocean.ocean import Ocean as SquidOcean

# from squid_py.config import Config
# from ocean_py import logger

class Ocean():

    def __init__(self, *args, **kwargs):
        """init the basic OceanClient for the connection and contract info"""
        self._config = OceanConfig(*args, **kwargs)

        # until 0.2.19
        # squid_config = Config(options_dict=self._config.as_squid_dict)
        # self._squid_ocean = SquidOcean(squid_config)

        self._squid_ocean = SquidOcean(config_dict=self._config.as_squid_dict)
        # For development, we use the HTTPProvider Web3 interface
        self._web3 = Web3(HTTPProvider(self._config.keeper_url))

        self._agent = None
        if self._config.agent_store_did:
            self._agent = self.resolve_agent(self._config.agent_store_did, authorization=self._config.agent_store_auth)

    def resolve_agent(self, agent_did, **kwargs):
        """
        Resolve an agent did or agent object
        :param agent_did: object or string of the agent or DID of the agent
        :param kwargs: optional args to pass to the agent

        :return: return the agent object that has been resolved, or None if no
        agent found for a DID.
        """
        if isinstance(agent_did, str):
            agent = MetadataAgent(self, did=agent_did, **kwargs)
        elif isinstance(agent_did, Agent):
            agent = agent_did
        else:
            raise ValueError('You must provide a did or an agent object to add too the library')
        return agent

    def register_asset_on_chain(self, metadata, **kwargs):
        """
        Register an on chain asset
        :param metadata: dict of the metadata
        :return The new asset registered, or return None on error
        """

        asset = AssetOnChain(self)
        if asset.register(metadata, **kwargs):
            return asset
        return None

    def register_asset_off_chain(self, metadata, **kwargs):
        """
        Register an asset on the off chain system using an metadata storage agent
        :return: the asset that has been registered
        """
        if not self._agent:
            raise ValueError('Please set the "agent_store_did" setting when starting the Ocean library')

        asset = AssetOffChain(self, agent=self._agent)
        if asset.register(metadata, **kwargs):
            return asset
        return None

    def get_asset(self, did):
        """
        :param: did: DID of the asset and agent combined.
        :return a registered asset given a DID of the asset
        """
        if AssetOnChain.is_did_valid(did):
            asset = AssetOnChain(self, did)
        elif AssetOffChain.is_did_valid(did):
            if not self._agent:
                raise ValueError('Please set the "agent_store_did" setting when starting the Ocean library')
            asset = AssetOffChain(self, did, agent=self._agent)


        if not asset.is_empty:
            if asset.read():
                return asset
        return None


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
