"""
    Asset class to handle the _other_ type of asset storage and addressing.

    **Currently this is in development**

"""
from starfish.metadata.metadata_object import MetadataObject

# from starfish import logger

class Metadata(MetadataObject):
    """

        :param ocean: agent object to used to creat
        :param did: Optional did of the asset.

    """
    def __init__(self, agent, metadata):
        """
        init an asset class with the following:
        """
        MetadataObject.__init__(self, agent, metadata)
