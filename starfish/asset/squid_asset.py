"""
    Squid Asset
"""

from starfish.asset import Asset

class SquidAsset(Asset):
    """

    Create a new squid asset to use in the Ocean network

    :param metadata: metadata to store for this asset, it must be a valid squid metadata dict
    :type metadata: dict
    :param did: did of the asset if it is registered, can be None for a new non registered asset
    :type did: None or str

    """
    def __init__(self, metadata, did=None):
        Asset.__init__(self, metadata, did)


