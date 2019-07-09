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
    def __init__(self, asset_type, metadata, did=None):
        """
        init an asset class
        """
        self._metadata = metadata
        self._metadata['type'] = asset_type
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

    def is_asset_type(self, type_name):
        """

        Returns if this metadata has the correct type

        :param str type_name: name of the asset type stored in the metadata

        :return: True if the metadata type is equal to type_name
        :type: boolean

        """
        asset_type = AssetBase.get_asset_type(self._metadata)
        return asset_type == type_name

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

    @property
    def params(self):
        return params

    @property
    def is_bundle(self):
        """

        Return True if this asset is a bundle asset and can contain sub assets ( Asset Bundle )

        :return: True if sub assets can be held within this asset
        :type: boolean

        """
        return False


    @staticmethod
    def merge_metadata(metadata, default_metadata):
        for name, value in default_metadata.items():
            if not name in metadata:
                metadata[name] = value
        return metadata

    @staticmethod
    def get_asset_type(metadata):
        asset_type = ''
        if isinstance(metadata, dict):
            if 'type' in metadata:
                asset_type = metadata['type']
            else:
                # if from squid then it's always a bundle
                if 'base' in metadata:
                    asset_type = 'bundle'
        return asset_type
