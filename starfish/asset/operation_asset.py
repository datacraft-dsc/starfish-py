"""
    Inovke Asset
"""

from starfish.asset.asset_base import AssetBase


class OperationAsset(AssetBase):

    """

    Operation asset can be used to perform a invokable service

    :param metadata: Optional dictionary metadata to provide for the asset
        if non used then the class will generate a default metadata based on the data provided
    :type metadata: None or dict
    :param did: Optional did of the asset if it's registered
    :type did: None or str

    """
    def __init__(self, metadata=None, did=None, metadata_text=None):
        if not isinstance(metadata, dict):
            raise ValueError('metadata must be a dict')

        AssetBase.__init__(self, metadata, did, metadata_text)

    def create(name, metadata=None, did=None):
        """

        Create a new OperationAsset.

        :param str name: Name of the asset
        :param dict metadata: Optional metadata to add to the assets metadata
        :param str did: Option DID to assign to this asset

        """
        metadata = AssetBase.generateMetadata(name, 'operation', metadata)
        return OperationAsset(metadata, did)

    def is_mode(self, mode_type):
        """

        Check to see if this operation supports the mode provided.

        :param str mode_type: Mode type to check to see if this operation supports
        :return: Return True if this mode is supported
        :type: boolean

        """
        try:
            return mode_type in self._metadata['operation']['modes']
        except ValueError:
            raise ValueError('Metadata does not contain operation->modes structure')
