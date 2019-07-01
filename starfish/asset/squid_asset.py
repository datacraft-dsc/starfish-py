"""
    Squid Asset
"""

from starfish.asset.asset_base import AssetBase

class SquidAsset(AssetBase):
    """

    Create a new squid asset to use in the Ocean network

    :param metadata: metadata to store for this asset, it must be a valid squid metadata dict
    :type metadata: dict
    :param did: did of the asset if it is registered, can be None for a new non registered asset
    :type did: None or str

    """

    def __init__(self, metadata=None, did=None, filename=None):
        AssetBase.__init__(self, 'squid', metadata, did)
