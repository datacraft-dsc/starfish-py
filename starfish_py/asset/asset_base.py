"""
    Asset class to hold Ocean asset information such as asset id and metadata
"""


# from starfish_py import logger

class AssetBase(object):
    def __init__(self, ocean, did=None, asset=None):
        """
        init an asset class with the following:
        :param ocean: ocean object to use to connect to the ocean network
        :param asset: opiton asset to copy from
        """
        self._ocean = ocean

        self._id = None
        self._did = did
        self._metadata = None

        if asset:
            self._id = asset.id
            self._did = asset.did
            self._metadata = asset.metadata

    def register(self, metadata):
        """ abstract method to register an asset"""

    def read(self):
        """ abstract method to read an asset """

    def copy(self):
        return AssetBase(self)

    @property
    def asset_id(self):
        """return the asset id"""
        return self._id

    @property
    def metadata(self):
        """ return the core metadata"""
        return self._metadata

    @property
    def is_empty(self):
        """ return true if empty asset """
        return self._id is None

    @property
    def id(self):
        """return the id of the asset"""
        return self._id
    @property
    def did(self):
        """return the DID of the asset"""
        return self._did

    @staticmethod
    def is_did_valid(did):
        """ return true if the did is valid for this asset type"""
        return False
