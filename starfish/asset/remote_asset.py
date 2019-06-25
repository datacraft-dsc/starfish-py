"""
    Memory Asset
"""

from starfish.asset.asset_base import AssetBase
from mimetypes import MimeTypes


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
        if metadata is None:
            metadata = {
                'name': 'RemoteAsset',
                'type': 'remote',
                'contentType': 'application/octet-stream',
                'url': url,
            }
        AssetBase.__init__(self, metadata, did)
        self._url = url

        mime = MimeTypes()
        mime_type = mime.guess_type(self.url)
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
