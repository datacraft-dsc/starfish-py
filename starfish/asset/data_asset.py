"""
    Memory Asset
"""
import os
from mimetypes import MimeTypes
from urllib.parse import urlparse


from starfish.asset.asset_base import AssetBase

class DataAsset(AssetBase):
    """

    File asset can be used manage a data asset on the ocean network

    :param metadata: Dictionary metadata to provide for the asset.
    :type metadata: None or dict
    :param did: Optional did of the asset if it's registered
    :type did: None or str
    :param str data: Optional data of the asset, this can be str or bytes

    """
    def __init__(self, metadata, did=None, data=None):
        if not isinstance(metadata, dict):
            raise ValueError('metadata must be a dict')

        if data:
            if not isinstance(data, str) or isinstance(data, bytes):
                raise ValueError('data can only be str or bytes')

        metadata['type'] = 'dataset'

        self._data = data
        AssetBase.__init__(self, metadata, did)

    @staticmethod
    def create(name, data, did=None):
        metadata = {
            'name': name,
            'type': 'dataset',
        }
        if isinstance(data, str):
            metadata['contentType'] = 'text/plain; charset=utf-8'
        elif isinstance(data, bytes):
            metadata['contentType'] = 'application/octet-stream'
        else:
            raise ValueError('data can only be str or bytes')
        metadata['size'] = 0
        if data:
            metadata['size'] = len(data)

        return DataAsset(metadata, did, data=data)

    @staticmethod
    def create_from_file(name, filename, did=None, is_read=True):
        metadata = {
            'name': name,
            'type': 'dataset',
        }
        data = None
        if os.path.exists(filename):
            mime = MimeTypes()
            mime_type = mime.guess_type(f'file://{self._filename}')
            if mime_type:
                metadata['contentType'] = mime_type[0]
            metadata['contentLength'] = os.path.getsize(self._filename)
            if is_read:
                with open(filename, 'rb') as fp:
                    data = fp.read()
        metadata['filename'] = os.path.basename(self._filename)
        metadata['size'] = 0
        if data:
            metadata['size'] = len(data)

        return DataAsset(metadata, did, data=data)

    @staticmethod
    def create_from_url(name, url, did=None):
        metadata = {
            'name': name,
            'type': 'dataset',
        }
        if urlparse(url):
            mime = MimeTypes()
            mime_type = mime.guess_type(url)
            if mime_type and mime_type[0]:
                metadata['contentType'] = mime_type[0]

        metadata['size'] = 0
        if url:
            metadata['size'] = len(url)

        return DataAsset(metadata, did, data=url)


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

