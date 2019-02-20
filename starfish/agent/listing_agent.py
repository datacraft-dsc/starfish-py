"""

Agent class to provide basic functionality for all Ocean Agents

"""

from starfish.agent import AgentObject

class ListingAgent(AgentObject):
    """

    Listing Agent class allows you to get and register listings.

    """

    def __init__(self, ocean):
        """init a standard ocean object"""
        AgentObject.__init__(self, ocean)


    def register(self, metadata, **kwargs):
        """

        Register an asset listing by writing it's listing and meta data to storage

        :param metadata: dict of the metadata.
        :param agent: agent object for perform meta stroage.

        :return: The new listing object
        :type: :class:`listing.Listing`
        """

        model = MetadataAgentModel(self._ocean)

        listing = None
        register_data = model.register_asset(metadata)
        if register_data:
            # assign the did of the agent that we registered this with
            data_id = asset_data['asset_id']
            did = f'{agent.did}/{data_id}'
            asset = Asset(did, metadata)
            listing = Listing(self, asset, None)
        return listing


    def get_asset(self, did):
        """

        Return an asset based on the asset's DID.

        :param str did: DID of the listng and agent combined.

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
