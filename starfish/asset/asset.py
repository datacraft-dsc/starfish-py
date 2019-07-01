"""
    Asset
"""

from starfish.asset.asset_base import AssetBase

class Asset(AssetBase):

    def __init__(self, metadata=None, did=None, filename=None):
        AssetBase.__init__(self, 'asset', metadata, did)
