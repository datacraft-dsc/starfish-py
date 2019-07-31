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

    :param metadata: Optional dictionary metadata to provide for the asset
        if non used then the class will generate a default metadata based on the data provided
    :type metadata: None or dict
    :param did: Optional did of the asset if it's registered
    :type did: None or str
    :param str filename: Optional filename of the asset
    :param str data: Optional data of the asset

    """
    def __init__(self, metadata=None, did=None, filename=None, data=None, url=None):
        default_metadata = {
            'name': 'Data asset',
            'type': 'dataset',
        }
        if metadata is None:
            metadata = default_metadata
        if not isinstance(metadata, dict):
            raise ValueError('metadata must be a dict')
        metadata = AssetBase.merge_metadata(metadata, default_metadata)

        if filename:
#            if not os.path.exists(filename):
#                raise NotFoundErr(f'File {filename} not found')
            if 'contentType' not in metadata and os.path.exists(filename):
                mime = MimeTypes()
                mime_type = mime.guess_type(f'file://{self._filename}')
                if mime_type:
                    metadata['contentType'] = mime_type[0]
                metadata['contentLength'] = os.path.getsize(self._filename)
            metadata['filename'] = os.path.basename(self._filename)

        if data and 'contentType' not in metadata:
            if isinstance(data, str):
                metadata['contentType'] = 'text/plain; charset=utf-8'
            else:
                metadata['contentType'] = 'application/octet-stream'


        if url and urlparse(url) and 'contentType' not in metadata:
            mime = MimeTypes()
            mime_type = mime.guess_type(self._url)
            if mime_type and mime_type[0]:
                metadata['contentType'] = mime_type[0]

        # data asset can have a filename and or data
        self._filename = metadata.get('filename', filename)
        self._url = metadata.get('url', url)
        self._data = data

        AssetBase.__init__(self, 'dataset', metadata, did)

    def save(self, filename):
        """
        Saves the data in the data asset to a file.

        :param str filename: Filename to save the data.

        """

        if self._data:
            with open(filename, 'wb') as fp:
                fp.write(self._data)

    @property
    def filename(self):
        """

        Return the asset data

        :return: the asset data
        :type: str or byte
        """
        return self._filename

    @property
    def data(self):
        if self._filename:
            if os.path.exists(self._filename):
                with open(self._filename, 'rb') as fp:
                    return fp.read()
        return self._data

    @property
    def url(self):
        """

        Return the asset data

        :return: the asset data
        :type: str or byte
        """
        return self._url
