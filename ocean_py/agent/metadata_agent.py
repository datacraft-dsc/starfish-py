"""
    MetadataAgent - Agent to access the off chain meta storage in squid aka Aquarius
"""

from ocean_py.agent.agent_base import AgentBase


# from ocean_py import logger

class MetadataAgent(AgentBase):
    def __init__(self, ocean):
        """init a standard ocean agent, with a given DID"""
        AgentBase.__init__(self, ocean)

    def register_asset(self, metadata, account):
        """
        Register an asset with the agent storage server
        :param metadata: metadata to write to the storage server
        :param account: account to register the asset
        """

        # TODO: we may need to see if we can pass our own service descriptors
        # instead of relying squid to create them for us.
        return self._ocean.squid.register_asset(metadata, account)

    def read_asset(self, did):
        """ read the asset metadata(DDO) using the asset DID """
        return self._ocean.squid.resolve_asset_did(did)

    def search_assets(self, text, sort=None, offset=100, page=0):
        ddo_list = self._ocean.squid.search_assets_by_text(text, sort, offset, page)
        print(ddo_list)
        return ddo_list
