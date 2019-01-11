"""
    Asset class to hold Ocean asset information such as asset id and metadata
"""


# from ocean_py import logger

class AssetBase():
    def __init__(self, ocean, did=None):
        """
        init an asset class with the following:
        :param ocean: ocean object to use to connect to the ocean network
        """
        self._ocean = ocean
        self._id = None
        self._metadata = None
        self._did = did


    def register(self, metadata, **kwargs):
        """ abstract method to register an asset"""
        pass

    def read(self):
        """ abstract method to read an asset """
        pass

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
    def did(self):
        """return the DID of the asset"""
        return self._did

    @staticmethod
    def is_did_valid(did):
        """ return true if the did is valid for this asset type"""
        return False
