"""
    Basic Ocean class to allow for registration and obtaining assets and agents

"""
from web3 import (
    Web3,
    HTTPProvider
)

from ocean_py.asset.asset import Asset
from ocean_py.asset.asset_light import AssetLight
from ocean_py.config import Config as OceanConfig
from ocean_py.agent.metadata_market_agent import MetadataMarketAgent
from ocean_py.agent.metadata_agent import MetadataAgent

from squid_py.ocean.ocean import Ocean as SquidOcean
from squid_py.config import Config

# from squid_py.config import Config
# from ocean_py import logger

class Ocean():

    def __init__(self, *args, **kwargs):
        """init the basic OceanClient for the connection and contract info"""
        self._config = OceanConfig(*args, **kwargs)

        squid_config = Config(options_dict=self._config.as_squid_dict)
        self._squid_ocean = SquidOcean(squid_config)

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

    def register_agent(self, agent_name, endpoint, account, did=None):
        """
        Register this agent on the block chain
        :param agent_name: agent object or name of the registration to use to register an agent
        :param endpoint: URL of the agents service to register
        :param account: Ethereum account to use as the owner of the DID->DDO registration
        :param did: DID of the agent to register, if it already exists
        :return private password of the signed DDO
        """
        
        name = None
        if isinstance(agent_name, Agent):
            name = agent_name.register_name
        elif isinstance(agent_name, str):
            name = agent_name

        if not name:
            raise ValueError('Provide an agent or a agent service name to register')
            
        if did is None:
            # if no did then we need to create a new one
            did = id_to_did(secrets.token_hex(32))

        # create a new DDO
        ddo = DDO(did)
        # add a signature
        private_key_pem = ddo.add_signature()
        # add the service endpoint with the meta data
        ddo.add_service(name, endpoint)
        # add the static proof
        ddo.add_proof(0, private_key_pem)
        if self.register_ddo(did, ddo, account):
            # save this to the object once the registration has occured
            self._did = did
            self._ddo = ddo
            return private_key_pem
        return None

    def register_asset(self, metadata, **kwargs):
        """
        Register an on chain asset
        :param metadata: dict of the metadata
        :return The new asset registered, or return None on error
        """

        asset = Asset(self)
        if asset.register(metadata, **kwargs):
            return asset
        return None

    def register_asset_light(self, metadata, **kwargs):
        """
        Register an asset on the off chain system using an metadata storage agent
        :return: the asset that has been registered
        """

        asset = AssetLight(self, **kwargs)
        if asset.register(metadata, **kwargs):
            return asset
        return None

    def get_asset(self, did, **kwargs):
        """
        :param: did: DID of the asset and agent combined.
        :return a registered asset given a DID of the asset
        """
        if Asset.is_did_valid(did):
            asset = Asset(self, did)
        elif AssetLight.is_did_valid(did):
            if not self._agent:
                raise ValueError('Please set the "agent_store_did" setting when starting the Ocean library')
            asset = AssetLight(self, did)
            
        if not asset.is_empty:
            if asset.read(**kwargs):
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
