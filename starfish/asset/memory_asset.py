"""
    Memory Asset
"""

from starfish.asset.asset_base import AssetBase

class MemoryAsset(AssetBase):
    """

    Memory asset can be used to try out assets without accessing any file system

    :param data: data string or byte text to save as the asset
    :type data: str or byte array
    :param metadata: Optional dictionary metadata to provide for the asset
        if non used then the class will generate a default metadata based on the data provided
    :type metadata: None or dict
    :param did: Optional did of the asset if it's registered
    :type did: None or str

    """
    def __init__(self, metadata=None, did=None, data=None):
        default_metadata = {
            'name': 'MemoryAsset',
            'type': 'data',
            'contentType': 'application/octet-stream',
        }
        if metadata is None:
            metadata = default_metadata
        if not isinstance(metadata, dict):
            raise ValueError('metadata must be a dict')
        metadata = AssetBase.merge_metadata(metadata, default_metadata)

        if data:
            if isinstance(data, str):
                metadata['contentType'] = 'text/plain; charset=utf-8'
            else:
                metadata['contentType'] = 'application/octet-stream'
        AssetBase.__init__(self, 'data', metadata, did)
        self._data = data

    def save(self, filename):
        """
        Saves the data in the memory asset to a file.

        :param str filename: Filename to save the data.

        """

        if self._data:
            with open(filename, 'wb') as fp:
                fp.write(self._data)

    @property
    def data(self):
        """

        Return the asset data

        :return: the asset data
        :type: str or byte
        """
        return self._data
