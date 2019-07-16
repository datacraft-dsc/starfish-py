"""
    Memory Asset
"""
import os
from mimetypes import MimeTypes

from starfish.asset.asset_base import AssetBase

class FileAsset(AssetBase):
    """

    File asset can be used manage a file asset on the ocean network

    :param metadata: Optional dictionary metadata to provide for the asset
        if non used then the class will generate a default metadata based on the data provided
    :type metadata: None or dict
    :param did: Optional did of the asset if it's registered
    :type did: None or str
    :param str filename: filename of the asset to register

    """
    def __init__(self, metadata=None, did=None, filename=None):
        default_metadata = {
            'name': 'FileAsset',
            'type': 'file',
            'author': 'File Asset',
            'contentType': 'application/octet-stream',
        }
        if metadata is None:
            metadata = default_metadata
        if not isinstance(metadata, dict):
            raise ValueError('metadata must be a dict')
        metadata = AssetBase.merge_metadata(metadata, default_metadata)

        AssetBase.__init__(self, 'file', metadata, did)
        if filename:
            self._filename = filename
            if not os.path.exists(filename):
                raise NotFoundErr(f'File {filename} not found')
            mime = MimeTypes()
            mime_type = mime.guess_type(f'file://{self._filename}')
            if mime_type:
                self._metadata['contentType'] = mime_type[0]
            self._metadata['contentLength'] = os.path.getsize(self._filename)
            self._metadata['filename'] = os.path.basename(self._filename)

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
        if os.path.exists(self._filename):
            with open(self._filename, 'rb') as fp:
                return fp.read()
