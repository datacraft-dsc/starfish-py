"""

    Memory Asset

"""

import os
from mimetypes import MimeTypes

from starfish.asset.asset_base import AssetBase
from starfish.utils.crypto_hash import hash_sha3_256


class DataAsset(AssetBase):
    """

    File asset can be used manage a data asset on the ocean network

    :param metadata: Dictionary metadata to provide for the asset.
    :type metadata: None or dict
    :param did: Optional did of the asset if it's registered
    :type did: None or str
    :param str data: Optional data of the asset, this can be str or bytes

    """
    def __init__(self, metadata, did=None, data=None,  metadata_text=None):
        if not isinstance(metadata, dict):
            raise ValueError('metadata must be a dict')

        if data:
            if not (isinstance(data, str) or isinstance(data, bytes)):
                raise ValueError('data can only be str or bytes')
            if not isinstance(data, bytes):
                data = data.encode('utf-8')

            metadata['contentHash'] = hash_sha3_256(data)
        metadata['type'] = 'dataset'

        self._data = data
        AssetBase.__init__(self, metadata, did, metadata_text)

    @staticmethod
    def create(name, data, metadata=None, did=None):
        """

        Create a new DataAsset using string or bytes data.

        :param str name: Name of the asset to create
        :param str, bytes data: Data to assign to the asset
        :param dict metadata: Optional metadata to add to the assets metadata
        :param str did: Option DID to assign to this asset

        :return: a new DataAsset
        :type: :class:`.DataAsset`

        """
        metadata = AssetBase.generateMetadata(name, 'dataset', metadata)
        if isinstance(data, str):
            metadata['contentType'] = 'text/plain; charset=utf-8'
        elif isinstance(data, bytes):
            metadata['contentType'] = 'application/octet-stream'
        else:
            raise ValueError('data can only be str or bytes')

        return DataAsset(metadata, did, data=data)

    @staticmethod
    def create_from_file(name, filename, metadata=None, did=None, is_read=True):
        """

        Create a new DataAsset using a file or filename.

        :param str name: Name of the asset to create
        :param str filename: If the filename is assigned to a valid file,
            the contents will be saved in the asset
        :param dict metadata: Optional metadata to add to the assets metadata
        :param str did: Option DID to assign to this asset
        :param bool is_read: If True read the file contents in as asset data.

        :return: a new DataAsset
        :type: :class:`.DataAsset`

        """

        metadata = AssetBase.generateMetadata(name, 'dataset', metadata)

        metadata['filename'] = str(filename)
        data = None
        if os.path.exists(filename):
            metadata['contentType'] = 'application/octet-stream'
            mime = MimeTypes()
            mime_type = mime.guess_type(f'file://{filename}')
            if mime_type:
                metadata['contentType'] = mime_type[0]
            if is_read:
                metadata['contentLength'] = os.path.getsize(filename)
                with open(filename, 'rb') as fp:
                    data = fp.read()
                metadata['size'] = len(data)

        return DataAsset(metadata, did, data=data)

    def save_to_file(self, filename):
        """
        Saves the data in the data asset to a file.

        :param str filename: Filename to save the data.

        """

        if self._data:
            with open(filename, 'wb') as fp:
                fp.write(self._data)

    @property
    def data(self):
        return self._data
