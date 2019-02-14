"""

Agent class to provide basic functionality for all Ocean Agents

"""

from starfish import Account
from starfish.models.squid_model import SquidModel

from starfish.ocean_object import OceanObject

class ListingAgent(OceanObject):
    """

    Listing Agent class allows you to get and register listings.

    """

    def __init__(self, ocean):
        """init a standard ocean object"""
        OceanObject.__init__(self, ocean)


    def register(self, metadata):
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
        

    def search(self, text, sort=None, offset=100, page=0):
        """

        Search the off chain storage for an asset with the givien 'text'

        :param str text: Test to search all metadata items for.
        :param sort: sort the results ( defaults: None, no sort).
        :type sort: str or None
        :param int offset: Return the result from with the maximum record count ( defaults: 100 ).
        :param int page: Returns the page number based on the offset.

        :return: a list of assets objects found using the search.
        :type: list of DID strings
        """
        pass
