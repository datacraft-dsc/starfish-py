"""
    Bundle Asset
"""
import json

from typing import (
    Any,
    Dict,
    Generic,
    Iterator,
    List
)


from starfish.asset.asset_base import AssetBase
from starfish.types import TBundleAsset


class BundleAsset(AssetBase, Generic[TBundleAsset]):
    """

    Bundle asset can be used to hold many assets

    :param metadata: Dictionary metadata to provide for the asset
    :type metadata: dict
    :param did: Optional did of the asset if it's registered
    :type did: None or str

    """
    def __init__(self, metadata_text: str) -> None:

        AssetBase.__init__(self, metadata_text)
        self._assets = {}
        metadata = json.loads(metadata_text)
        if 'contents' in metadata:
            for name, item in metadata['contents'].items():
                self._assets[name] = item['assetID']

    @staticmethod
    def create(name: str, asset_list: any = None, metadata: Any = None) -> TBundleAsset:
        """

        Create a new empty BundleAsset

        :param str name: Name of the asset to create
        :param dict asset_list: List of assets and their names
        :param dict metadata: Optional metadata to add to the assets metadata
        :param str did: Option DID to assign to this asset

        :return: a new BundleAsset
        :type: :class:`.BundleAsset`
        """

        metadata = AssetBase.generateMetadata(name, 'bundle', metadata)
        if asset_list:
            metadata['contents'] = {}
            for name, asset_id in asset_list.items():
                metadata['contents'][name] = {
                    'assetId': asset_id
                }

        return BundleAsset(json.dumps(metadata))

    def add(self, name: str, asset: AssetBase) -> None:
        """

        Add an asset to the bundle. Any asset object

        :param string name: name of the asset in the bundle
        :param asset: asset to add to the bundle collection
        :type asset: :class:`.Asset` object

        """

        if not isinstance(name, str):
            raise TypeError('You need to pass the asset name as a string')
        if not isinstance(asset, AssetBase):
            raise TypeError('You need to pass an Asset object')

        self._assets[name] = asset.asset_id
        self._rebuild_metadata(self._assets)

    def get_asset_id(self, name: str) -> str:
        """

        Return the asset in the bundle based on it's index number

        :param str name: name of the asset in this bundle

        :return: asset id is returned
        :type: str

        :raises: ValueError if name is not found in the bundle
        """
        if isinstance(name, str):
            if name not in self._assets:
                raise ValueError(f'Cannot find asset named {name}')
        if isinstance(name, int):
            if name < 0 or name > self.asset_count:
                raise ValueError(f'Cannot find asset at index {name}')
            name = self.asset_names[name]
        return self._assets[name]

    def asset_remove(self, name: str) -> str:
        """

        Remove an asset from the bundle with a given name

        :param str name: name of the asset to remove
        :return: the removed asset id
        :type: str

        """
        if self._assets is None or name not in self._assets:
            raise ValueError(f'Cannot find asset named {name}')
        asset = self._assets[name]
        del self._assets[name]
        self._rebuild_metadata(self._assets)

        return asset

    def __iter__(self) -> Iterator[str]:
        """

        Iterator method. This allows you to do the following::

            for index, asset in bundle:
                print('my assets in the bundle are', index, asset)
        """
        self._iter_index = 0
        return self

    def __next__(self) -> str:
        """

        Provide the __next__ method of a iterator.

        :return: index, asset
        :type: int, :class:.`Asset` object

        """
        if self._iter_index < self.asset_count:
            index = self._iter_index
            name = self.asset_names[index]
            asset = self._assets[name]
            self._iter_index += 1
            return name, asset
        else:
            raise StopIteration

    def __getitem__(self, name: str) -> AssetBase:
        return self._assets[name]

    def get_asset_id_at_index(self, index) -> str:
        """ return the asset based on the index of available assets """
        return list(self._assets.values())[index]

    def _rebuild_metadata(self, asset_list):
        metadata = self.metadata
        metadata['contents'] = {}
        for name, asset_id in asset_list.items():
            metadata['contents'][name] = {
                'assetId': asset_id
            }
        self.set_metadata(metadata)

    @property
    def asset_count(self) -> int:
        """

        Return the number of assets in this bundle

        :return: count of assets
        :type: int
        """
        return len(self._assets.keys())

    @property
    def asset_items(self) -> Dict[str, str]:
        return self._assets.items()

    @property
    def asset_names(self) -> List[str]:
        return list(self._assets.keys())

    @property
    def is_bundle(self) -> bool:
        """

        Return True if this asset is a bundle asset and can contain sub assets ( Asset Bundle )

        :return: True if sub assets can be held within this asset
        :type: boolean

        """
        return True
