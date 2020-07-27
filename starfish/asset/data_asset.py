"""

    Memory Asset

"""
import json
import os
from mimetypes import MimeTypes
from typing import (
    Any,
    Generic
)

from starfish.asset.asset_base import AssetBase
from starfish.types import TDataAsset
from starfish.utils.crypto_hash import hash_sha3_256


class DataAsset(AssetBase, Generic[TDataAsset]):
    """

    File asset can be used manage a data asset on the dex network

    :param metadata: Dictionary metadata to provide for the asset.
    :type metadata: None or dict
    :param did: Optional did of the asset if it's registered
    :type did: None or str
    :param str data: Optional data of the asset, this can be str or bytes

    """
    def __init__(self, metadata_text: str, data: Any = None) -> None:

        if data:
            if not (isinstance(data, str) or isinstance(data, bytes)):
                raise ValueError('data can only be str or bytes')
            if not isinstance(data, bytes):
                data = data.encode('utf-8')

        self._data = data
        AssetBase.__init__(self, metadata_text)

    @staticmethod
    def create(name: str, data: Any, metadata: Any = None) -> TDataAsset:
        """

        Create a new DataAsset using string or bytes data.

        :param str name: Name of the asset to create
        :param str, bytes data: Data to assign to the asset
        :param dict metadata: Optional metadata to add to the assets metadata

        :return: a new DataAsset
        :type: :class:`.DataAsset`

        """
        if metadata is None:
            metadata = {}
        if isinstance(data, str):
            metadata['contentType'] = 'text/plain; charset=utf-8'
        elif isinstance(data, bytes):
            metadata['contentType'] = 'application/octet-stream'
        else:
            raise ValueError('data can only be str or bytes')

        metadata['contentHash'] = hash_sha3_256(data)

        metadata = AssetBase.generateMetadata(name, 'dataset', metadata)
        return DataAsset(json.dumps(metadata), data=data)

    @staticmethod
    def create_from_file(name: str, filename: str, metadata: Any = None, did: str = None, is_read: bool = True) -> TDataAsset:
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
        metadata['contentHash'] = hash_sha3_256(data)
        metadata = AssetBase.generateMetadata(name, 'dataset', metadata)

        return DataAsset(json.dumps(metadata), data=data)

    def save_to_file(self, filename: str) -> None:
        """
        Saves the data in the data asset to a file.

        :param str filename: Filename to save the data.

        """

        if self._data:
            with open(filename, 'wb') as fp:
                fp.write(self._data)

    @property
    def data(self) -> Any:
        return self._data
