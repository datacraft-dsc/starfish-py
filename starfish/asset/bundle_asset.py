"""
    Bundle Asset
"""

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
    def __init__(self, metadata: Any, did: str = None, metadata_text: str = None) -> None:

        if not isinstance(metadata, dict):
            raise ValueError('metadata must be a dict')
        AssetBase.__init__(self, metadata, did, metadata_text)
        self._assets = {}

    @staticmethod
    def create(name: str, metadata: Any = None, did: str = None) -> TBundleAsset:
        """

        Create a new empty BundleAsset

        :param str name: Name of the asset to create
        :param dict metadata: Optional metadata to add to the assets metadata
        :param str did: Option DID to assign to this asset

        :return: a new BundleAsset
        :type: :class:`.BundleAsset`
        """

        metadata = AssetBase.generateMetadata(name, 'bundle', metadata)
        return BundleAsset(metadata, did)

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

        self._assets[name] = asset

    def get_asset(self, name: str) -> AssetBase:
        """

        Return the asset in the bundle based on it's index number

        :param str name: name of the asset in this bundle

        :return: asset is returned
        :type: :class:`.Asset` object

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

    def asset_remove(self, name: str) -> AssetBase:
        """

        Remove an asset from the bundle with a given name

        :param str name: name of the asset to remove
        :return: the removed asset
        :type: :class:`.Asset` object

        """
        if self._assets is None or name not in self._assets:
            raise ValueError(f'Cannot find asset named {name}')
        asset = self._assets[name]
        del self._assets[name]
        return asset

    def __iter__(self) -> Iterator[AssetBase]:
        """

        Iterator method. This allows you to do the following::

            for index, asset in bundle:
                print('my assets in the bundle are', index, asset)
        """
        self._iter_index = 0
        return self

    def __next__(self) -> AssetBase:
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

    def get_asset_at_index(self, index):
        """ return the asset based on the index of available assets """
        return list(self._assets.values())[index]

    @property
    def asset_count(self) -> int:
        """

        Return the number of assets in this bundle

        :return: count of assets
        :type: int
        """
        return len(self._assets.keys())

    @property
    def asset_items(self) -> Dict[str, AssetBase]:
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
