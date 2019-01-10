"""
    Basic Ocean class to allow for registration and obtaining assets and agents

"""
import secrets

from web3 import (
    Web3,
    HTTPProvider
)

from ocean_py.config import Config
from ocean_py.asset.asset_on_chain import AssetOnChain
from ocean_py.asset.asset_off_chain import AssetOffChain
from ocean_py.config import Config as OceanConfig
from ocean_py import logger


from squid_py.did import id_to_did
from squid_py.ocean.ocean import Ocean as SquidOcean
from squid_py.keeper import Keeper
from squid_py.config import Config


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

    def register_asset_on_chain(self, metadata, account, service=None, price=None, timeout=900):
        """
        Register an asset by writing it's meta data to the meta storage agent
        :param metadata: dict of the metadata
        :return The new asset registered, or return None on error
        """

        asset = AssetOnChain(self)
        if asset.register(metadata, account, service, price):
            return asset
        return None

    def get_asset(self, did):

        """
        :param: did: DID of the asset and agent combined.
        :param: agent: agent object to return meta data info for the asset,
        if None then the agent can be assigned earlier with this library.

        :return a registered asset given a DID of the asset"""
        
        if AssetOnChain.is_did_valid(did):
            asset = AssetOnChain(self, did)
        elif AssetOffChain.is_did_valid(did):
            asset = AssetOffChain(self, did)
        
        
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
        return self._squid_ocean
