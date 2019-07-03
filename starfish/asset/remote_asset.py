"""
    Memory Asset
"""

from starfish.asset.asset_base import AssetBase
from mimetypes import MimeTypes
from urllib.parse import urlparse


class RemoteAsset(AssetBase):
    """

    Remote asset can be used manage a remote asset using an URL on the ocean network

    :param metadata: Optional dictionary metadata to provide for the asset
        if non used then the class will generate a default metadata based on the data provided
    :type metadata: None or dict
    :param did: Optional did of the asset if it's registered
    :type did: None or str
    :param str filename: filename of the asset to register

    """
    def __init__(self, metadata=None, did=None, url=None):
        default_metadata = {
            'name': 'RemoteAsset',
            'type': 'remote',
            'contentType': 'application/octet-stream',
            'url': url,
        }
        if metadata is None:
            metadata = default_metadata
        if not isinstance(metadata, dict):
            raise ValueError('metadata must be a dict')
        metadata = AssetBase.merge_metadata(metadata, default_metadata)

        AssetBase.__init__(self, 'remote', metadata, did)
        self._url = metadata.get('url', url)

        if self._url and urlparse(self._url):
            mime = MimeTypes()
            mime_type = mime.guess_type(self._url)
            if mime_type and mime_type[0]:
                self._metadata['contentType'] = mime_type[0]

    @property
    def url(self):
        """

        Return the asset data

        :return: the asset data
        :type: str or byte
        """
        return self._url
