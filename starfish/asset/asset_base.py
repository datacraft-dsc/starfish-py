"""
    Asset class to handle core imutable asset and it's metadata


"""

import json
from abc import ABC
from starfish.utils.did import did_to_asset_id

class AssetBase(ABC):
    """

    :param str metadata_text: metadata text for the asset
    :param did: Octional did of the asset, if the asset is new then the did will be None.
    :type did: None or str

    """
    def __init__(self, metadata, did=None, metadata_text=None):
        """
        init an asset class
        """

        if not isinstance(metadata, dict):
            raise ValueError('metadata must be a dict')

        self._metadata = metadata
        self._metadata_text = metadata_text

        if self._metadata_text is None:
            self._metadata_text = json.dumps(metadata)

        if 'name' not in metadata:
            raise ValueError('metadata must contain a metadata name')

        if 'type' not in metadata:
            raise ValueError('metadata must contain a metadata type')

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
    def metadata_text(self):
        """
        :return: The metadata for this asset
        :type: dict
        """
        return self._metadata_text

    @property
    def asset_id(self):
        if self._did:
            return did_to_asset_id(self._did)
        return None

    @property
    def name(self):
        return self._metadata['name']

    @property
    def type_name(self):
        return self._metadata['type']

    @property
    def is_bundle(self):
        """

        Return True if this asset is a bundle asset and can contain sub assets ( Asset Bundle )

        :return: True if sub assets can be held within this asset
        :type: boolean

        """
        return False


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

    @staticmethod
    def generateMetadata(name, asset_type, metadata=None):
        if metadata is None:
            metadata = {}
        if not isinstance(metadata, dict):
            raise ValueError('The metadata has to be a dict')

        metadata['name'] = name
        metadata['type'] = asset_type
        return metadata
