"""
    Asset class to handle core imutable asset and it's metadata


"""

import json
from abc import ABC
from typing import (
    Any,
    Generic
)

from starfish.types import TAssetBase
from starfish.utils.crypto_hash import hash_sha3_256


class AssetBase(ABC, Generic[TAssetBase]):
    """

    :param str metadata_text: metadata text for the asset
    :param did: Octional did of the asset, if the asset is new then the did will be None.
    :type did: None or str

    """
    def __init__(self, metadata_text: str, did: str = None) -> None:
        """
        init an asset class
        """

        if isinstance(metadata_text, bytes):
            metadata_text = metadata_text.decode('utf-8')

        if not isinstance(metadata_text, str):
            raise TypeError('metadata must be in text form')

        self._metadata_text = metadata_text
        self._did = did

        if 'name' not in self.metadata:
            raise ValueError('metadata must contain a metadata name')

        if 'type' not in self.metadata:
            raise ValueError('metadata must contain a metadata type')

        super().__init__()

    def is_asset_type(self, type_name: str) -> bool:
        """

        Returns if this metadata has the correct type

        :param str type_name: name of the asset type stored in the metadata

        :return: True if the metadata type is equal to type_name
        :type: boolean

        """
        asset_type = AssetBase.get_asset_type(self.metadata)
        return asset_type == type_name

    @property
    def did(self) -> str:
        """
        :return: the asset did
        :type: str
        """
        return self._did

    @property
    def metadata(self) -> Any:
        """

        WARNING: The read only version for this metadata, use `set_metadata` to assign a new metadata.
        Once you change metadata, the asset id is changed and the did is set to None.

        :return: The metadata for this asset
        :type: dict
        """
        return json.loads(self._metadata_text)

    @property
    def metadata_text(self) -> str:
        """
        :return: The metadata for this asset
        :type: dict
        """
        return self._metadata_text

    @property
    def asset_id(self) -> str:
        return AssetBase.calc_asset_id(self._metadata_text)

    @property
    def name(self) -> str:
        return self.metadata.get('name', None)

    @property
    def type_name(self) -> str:
        return self.metadata.get('type', None)

    @property
    def is_bundle(self) -> bool:
        """

        Return True if this asset is a bundle asset and can contain sub assets ( Asset Bundle )

        :return: True if sub assets can be held within this asset
        :type: boolean

        """
        return False

    @property
    def is_new(self) -> bool:
        """

        Return True if this asset has not been saved, and can be changed.

        :return: True if no did has been set

        """
        return self._did is None

    @property
    def data(self) -> bytes:
        return None

    @staticmethod
    def get_asset_type(metadata: Any) -> str:
        asset_type = None
        if isinstance(metadata, dict):
            asset_type = metadata.get('type', None)
        return asset_type

    @staticmethod
    def generateMetadata(name: str, asset_type: str, metadata: Any = None) -> Any:
        if metadata is None:
            metadata = {}
        if not isinstance(metadata, dict):
            raise ValueError('The metadata has to be a dict')

        metadata['name'] = name
        metadata['type'] = asset_type
        return metadata

    @staticmethod
    def calc_asset_id(metadata_text):
        return hash_sha3_256(metadata_text)
