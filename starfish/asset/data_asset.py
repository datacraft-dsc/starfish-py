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
    def __init__(self, metadata_text: str, did: str = None, data: Any = None) -> None:

        AssetBase.__init__(self, metadata_text, did)
        if data:
            if isinstance(data, (str, bytes)):
                if isinstance(data, str):
                    data = data.encode('utf-8')
            else:
                raise TypeError('data can only be str or bytes')

        self._data = data

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
        metadata = AssetBase.generateMetadata(name, 'dataset', metadata)
        metadata = DataAsset.set_metadata_content_data(metadata, data=data)
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

        metadata = AssetBase.generateMetadata(name, 'dataset', metadata)
        if 'filename' not in metadata:
            metadata['filename'] = os.path.basename(str(filename))
        data = None
        if os.path.exists(filename):
            content_type = 'application/octet-stream'
            mime = MimeTypes()
            mime_type = mime.guess_type(f'file://{filename}')
            if mime_type:
                content_type = mime_type[0]
            if is_read:
                with open(filename, 'rb') as fp:
                    data = fp.read()
            metadata = DataAsset.set_metadata_content_data(metadata, data=data, content_type=content_type)

        return DataAsset(json.dumps(metadata), data=data)

    @staticmethod
    def set_metadata_content_data(metadata: dict, data: Any, content_type: str = None) -> dict:
        """

        Static method to generate the metadata values associated with storing data with an asset.

        This method will try to assign 'contentType', 'contentHash', 'contentLength' in the metadata dict

        :param dict metadata: Metadata to assign and return
        :param str,bytes data: Data to get the hash and length from
        :param str content_type: Optional content_type, if not provided the data will be used to determin the contentType

        :returns: a modified metadata dict with the new fields set

        """
        if not isinstance(metadata, dict):
            raise TypeError('you must assign a dict as the metadata to set the content data metadata')

        if content_type is None:
            content_type = 'application/octet-stream'
            if isinstance(data, str):
                content_type = 'text/plain'
            elif isinstance(data, bytes):
                content_type = 'application/octet-stream'
            else:
                raise ValueError('data can only be str or bytes')

            # test for json
            try:
                json_data = json.loads(data)
                if json_data:
                    content_type = 'application/json'
            except ValueError:
                pass

        if 'contentType' not in metadata and content_type:
            metadata['contentType'] = content_type
        if data:
            if 'contentHash' not in metadata:
                metadata['contentHash'] = hash_sha3_256(data)
            if 'contentLength' not in metadata:
                metadata['contentLength'] = len(data)
        return metadata

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
