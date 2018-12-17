"""
    Basic Ocean class to allow for registration and obtaining assets and agents

"""
import secrets

from web3 import (
    Web3,
    HTTPProvider
)

from ocean_py.config import Config
from ocean_py.asset import Asset
from ocean_py.agent import Agent
from ocean_py.config import Config
from ocean_py import logger


from squid_py.did import id_to_did
from squid_py.ocean.ocean import Ocean as SquidOcean
from squid_py.keeper import Keeper


class Ocean():

    def __init__(self, *args, **kwargs):
        """init the basic OceanClient for the connection and contract info"""
        self._config = Config(*args, **kwargs)
        # self._squid_ocean = SquidOcean(config_dict=self._config.as_squid_dict) - not ready yet in release
        self._squid_ocean = SquidOcean(config_file=self._config.as_squid_file)

        # For development, we use the HTTPProvider Web3 interface
        self._web3 = Web3(HTTPProvider(self._config.keeper_url))

        # With the interface loaded, the Keeper node is connected with all contracts
        self._keeper = Keeper(self._web3, self._config.contract_path)
        
        self._agents = {}


    def assign_agent(self, agent):
        """
        Assigns the agent to the local memory storage for use in later tasks
        """
        if not isinstance(agent, Agent):
            raise ValueError('You must provide an agent object to assign')
        self._agents[agent.did] = agent
        return agent.did
        

    def register_asset(self, metadata, did=None, agent=None):
        """
        Register an asset by writing it's meta data to the meta storage agent
        :param metadata: dict of the metadata
        :param did: did of the meta storage agent
        :return The new asset registered, or return None on error
        """
        
        if agent is None:
            # no agent so we need to see if it's assigned
            agent = self.get_agent(did)
        
        if agent is None:
            raise ValueError('Please provide a agent object or a did of an assigned agent')
            
            
        asset = Asset(self)
        if asset.register(metadata, agent):
            return asset
        return None


    def get_agent(self, did):
        # no agent so we need to see if it's assigned
        agent = self._agents[did]        
        return agent
        
    def get_asset(self, did, agent = None):
        
        """
        :param: did: DID of the asset and agent combined.
        :param: agent: agent object to return meta data info for the asset, 
        if None then the agent can be assigned earlier with this library.
        
        :return a registered asset given a DID of the asset"""
        asset = Asset(self, did)
        if not asset.is_empty:
            if asset.read_metadata(agent):
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
        return self._keeper

    @property
    def agents(self):
        return self._agents
