"""
    Asset class to handle core imutable asset and it's metadata


"""


from abc import ABC
from starfish.utils.did import did_to_asset_id

class AssetBase(ABC):
    """

    :param dict metadata: metadata for the asset
    :param did: Octional did of the asset, if the asset is new then the did will be None.
    :type did: None or str

    """
    def __init__(self, metadata, did=None):
        """
        init an asset class
        """
        self._metadata = metadata
        self._did = did
        super().__init__()


    def set_did(self, did):
        """
        This method makes the object immutable.
        So maybe a solution is that we have a 'copy' and
        set the did in the __init__ of the new class, to return a mutable copy of the
        same asset object.
        """
        self._did = did

    @property
    def did(self):
        """
        :return: the asset did
        :type: str
        """
        return self._did

    @property
    def metadata(self):
        """
        :return: The metadata for this asset
        :type: dict
        """
        return self._metadata

    @property
    def asset_id(self):
        if self._did:
            return did_to_asset_id(self._did)
        return None

    @property
    def data(self):
        return None
