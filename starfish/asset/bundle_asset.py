"""
    Bundle Asset
"""

from starfish.asset.asset_base import AssetBase

class BundleAsset(AssetBase):
    """

    Bundle asset can be used to hold many assets

    :param data: data string or byte text to save as the asset
    :type data: str or byte array
    :param metadata: Optional dictionary metadata to provide for the asset
        if non used then the class will generate a default metadata based on the data provided
    :type metadata: None or dict
    :param did: Optional did of the asset if it's registered
    :type did: None or str

    """
    def __init__(self, metadata=None, did=None, data=None):
        if metadata is None:
            metadata = {}
            metadata['name'] = 'BundleAsset'
            metadata['description'] = 'Bundle Asset'
        AssetBase.__init__(self, metadata, did)
        self._asset_list = []
        self._data = data

    def add(self, asset):
        """
        
        Add an asset to the bundle. Any asset object
        
        :param asset: asset to add to the bundle collection
        :type asset: :class:`.Asset` object
        
        :return: index of the new asset in the list
        :type: int

        """
        if not isinstance(asset, AssetBase):
            raise TypeError('You need to pass an Asset object')
        
        self._asset_list.append(asset)
        return(self.count - 1)

    def get_asset(self, index):
        """
        
        Return the asset in the bundle based on it's index number
        
        :param int index: index of the asset
        
        :return: asset is returned
        :type: :class:`.Asset` object
        
        :raises: IndexError if index is out of range
        """
        if index < 0 and index >= self.count:
            raise IndexError('Invalid asset index in asset bundle')
        return self._asset_list[index]
        
    def remove(self, index):
        """
        
        Remove an asset from the bundle
        
        :param int index: index of the asset to remove
        :return: the removed asset
        :type: :class:`.Asset` object

        """
        if index < 0 and index >= self.count:
            raise ValueError('Invalid asset index in asset bundle')
        return self._asset_list.pop(index)
        
    def pop(self, index=None):
        """
        
        pop an asset from the bundle
        
        :param int index: index of the asset to pop, can be empty to remove the last item
        :return: the poped asset
        :type: :class:`.Asset` object

        """
        if index is None:
            index = self.count - 1
        if index < 0 and index >= self.count:
            raise ValueError('Invalid asset index in asset bundle')
        return self._asset_list.pop(index)


    def __iter__(self):
        """
        
        Iterator method. This allows you to do the following::
        
            for index, asset in bundle:
                print('my assets in the bundle are', index, asset)
        """
        self._iter_index = 0
        return self
    
    def __next__(self):
        """
        
        Provide the __next__ method of a iterator.
        
        :return: index, asset
        :type: int, :class:.`Asset` object
        
        """
        if self._iter_index < self.count:
            index = self._iter_index
            asset = self._asset_list[index]
            self._iter_index += 1
            return index, asset
        else:
            raise StopIteration
            
    def __getitem__(self, key):
        return self._asset_list[key]
        
    @property
    def count(self):
        """
        
        Return the number of assets in this bundle
        
        :return: count of assets
        :type: int
        """
        return len(self._asset_list)
        
    @property
    def data(self):
        """

        Return the asset data

        :return: the asset data
        :type: str or byte
        """
        return self._data
