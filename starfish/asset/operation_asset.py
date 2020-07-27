"""
    Inovke Asset
"""
import json
from typing import (
    Any,
    Generic
)

from starfish.asset.asset_base import AssetBase
from starfish.types import TOperationAsset


class OperationAsset(AssetBase, Generic[TOperationAsset]):

    """

    Operation asset can be used to perform a invokable service

    :param metadata: Optional dictionary metadata to provide for the asset
        if non used then the class will generate a default metadata based on the data provided
    :type metadata: None or dict
    :param did: Optional did of the asset if it's registered
    :type did: None or str

    """
    def __init__(self, metadata_text: str) -> None:
        AssetBase.__init__(self, metadata_text)

    def create(name: str, metadata: Any = None) -> TOperationAsset:
        """

        Create a new OperationAsset.

        :param str name: Name of the asset
        :param dict metadata: Optional metadata to add to the assets metadata
        :param str did: Option DID to assign to this asset

        """
        metadata = AssetBase.generateMetadata(name, 'operation', metadata)
        return OperationAsset(json.dumps(metadata))

    def is_mode(self, mode_type: str) -> bool:
        """

        Check to see if this operation supports the mode provided.

        :param str mode_type: Mode type to check to see if this operation supports
        :return: Return True if this mode is supported
        :type: boolean

        """
        try:
            return mode_type in self.metadata['operation']['modes']
        except ValueError:
            raise ValueError('Metadata does not contain operation->modes structure')
