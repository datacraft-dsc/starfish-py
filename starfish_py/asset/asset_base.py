"""
    Asset base class
"""


# from starfish_py import logger

class AssetBase(object):
    """
    init an asset class with the following:

    :param ocean: ocean object to use to connect to the ocean network.
    :param did: Optional DID of the asset.
    :param asset: Optional asset to copy from.
    """

    def __init__(self, ocean, did=None, asset=None):
        """
        init an asset class with the following:
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
        """

        abstract method to register an asset

        """

    def read(self):
        """

        abstract method to read an asset

        """

    def copy(self):
        """

        :return: a copy of ourselves.
        """
        return AssetBase(self)

    @property
    def asset_id(self):
        """
        :return: the asset id.
        """
        return self._id

    @property
    def metadata(self):
        """
        :return: the core metadata.
        """
        return self._metadata

    @property
    def is_empty(self):
        """
        :return: true if empty asset.
        """
        return self._id is None

    @property
    def id(self):
        """
        :return: the id of the asset.
        """
        return self._id
    @property
    def did(self):
        """
        :return: the DID of the asset.
        """
        return self._did

    @staticmethod
    def is_did_valid(did):
        """
        :return;: True if the did is valid for this asset type
        """
        return False
