"""
    Asset class to handle the _other_ type of asset storage and addressing.

    **Currently this is in development**

"""
from starfish.metadata.metadata_object import MetadataObject

# from starfish import logger

class Metadata(MetadataObject):
    """

    :param agent: agent object to used to create
    :type agent: :class:`.AgentObject`
    :param metadata: Metadata.
    :type metadata: dict

    """
    def __init__(self, agent, metadata):
        """
        init an asset class with the following:
        """
        MetadataObject.__init__(self, agent, metadata)
