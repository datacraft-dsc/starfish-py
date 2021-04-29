"""
    Inovke Asset
"""
import json
from typing import (
    Any,
    Generic
)

from starfish.asset.asset_base import AssetBase
from starfish.asset.data_asset import DataAsset
from starfish.types import TOperationAsset


class OperationAsset(DataAsset, Generic[TOperationAsset]):

    """

    Operation asset can be used to perform a invokable service

    :param metadata: Optional dictionary metadata to provide for the asset
        if non used then the class will generate a default metadata based on the data provided
    :type metadata: None or dict
    :param did: Optional did of the asset if it's registered
    :type did: None or str
    :param str, bytes data: Optional data to assign to this operation asset

    """
    def __init__(self, metadata_text: str, did: str = None, data: Any = None) -> None:
        DataAsset.__init__(self, metadata_text, did=did, data=data)

    @staticmethod
    def create(name: str, metadata: Any = None, data: Any = None, modes: Any = None) -> TOperationAsset:
        """

        Create a new OperationAsset.

        :param str name: Name of the asset
        :param dict metadata: Optional metadata to add to the assets metadata
        :param str, bytes data: Option data to pass to the operation asset
        :param list,tuple modes: Modes supported by this opreation, defaults to ['sync', 'async']

        :returns OperationAsset object

        """
        metadata = AssetBase.generateMetadata(name, 'operation', metadata)
        if 'operation' not in metadata:
            metadata['operation'] = {}
        if modes is None:
            modes = ['sync', 'async']
        metadata['modes'] = modes
        if not isinstance(modes, (tuple, list)):
            raise TypeError(f'modes {modes} must be a list or tuple of the operation modes supported')

        return OperationAsset(json.dumps(metadata), data=data)

    @staticmethod
    def create_orchestration(name: str, data: Any = None, metadata: Any = None, modes: Any = None) -> TOperationAsset:
        """

        Create a new OperationAsset with a class of orchestration.

        :param str name: Name of the asset
        :param str, bytes data: Option orchestration dict or json str to pass to the operation asset
        :param dict metadata: Optional metadata to add to the assets metadata
        :param list,tuple modes: Modes supported by this opreation, defaults to ['sync', 'async']

        :returns OperationAsset object

        """
        data_text = None
        if data:
            if isinstance(data, dict):
                data_text = json.dumps(data)
            elif isinstance(data, (str, bytes)):
                data_text = data
            else:
                raise TypeError('ochestration data can only be json str, bytes or a dict')

        metadata = AssetBase.generateMetadata(name, 'operation', metadata)
        if data_text:
            metadata = DataAsset.set_metadata_content_data(metadata, data=data_text, content_type='application/json')

        if 'operation' not in metadata:
            metadata['operation'] = {}
        metadata['operation']['class'] = 'orchestration'

        if modes is None:
            modes = ['sync', 'async']
        if not isinstance(modes, (tuple, list)):
            raise TypeError(f'modes {modes} must be a list or tuple of the operation modes supported')

        metadata['modes'] = modes

        return OperationAsset(json.dumps(metadata), data=data_text)

    def is_mode(self, mode_type: str) -> bool:
        """

        Check to see if this operation supports the mode provided.

        :param str mode_type: Mode type to check to see if this operation supports
        :return: Return True if this mode is supported
        :type: boolean

        """
        try:
            if 'operation' in self.metadata and self.metadata['operation']:
                return mode_type in self.metadata['operation'].get('modes', [])
        except ValueError:
            raise ValueError('Metadata does not contain operation->modes structure')

    @property
    def is_orchestration(self):
        """

        Return true if this operation asset is an orchestration
        """

        return self.class_name == 'orchestration'

    @property
    def class_name(self):
        """

        Return operation class type name , for the orchestration this will be 'orchestration'
        """
        if 'operation' in self.metadata and self.metadata['operation']:
            return self.metadata['operation'].get('class', None)
