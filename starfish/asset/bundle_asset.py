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
            metadata['size'] = len(data)
            if isinstance(data, str):
                metadata['contentType'] = 'text/plain; charset=utf-8'
            else:
                metadata['contentType'] = 'application/octet-stream'
        AssetBase.__init__(self, metadata, did)
        self._data = data

    @property
    def data(self):
        """

        Return the asset data

        :return: the asset data
        :type: str or byte
        """
        return self._data
