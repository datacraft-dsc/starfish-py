

from starfish.asset.asset_base import AssetBase
from starfish.asset.memory_asset import MemoryAsset
from starfish.asset.bundle_asset import BundleAsset
from starfish.asset.operation_asset import OperationAsset
from starfish.asset.file_asset import FileAsset
from starfish.asset.remote_asset import RemoteAsset
from starfish.asset.asset import Asset


def create_asset_from_metadata(metadata, did=None):
    """
    Create a new asset class based on the metadata. Once created assign
    the metadata to the asset and also the optional did

    :param dict metadata: metadata to test and create the correct asset object
    :param str did: optional did to assign to the asset

    :return: Return an asset class based on the metadata type
    """

    asset_type = AssetBase.get_asset_type(metadata)

    if asset_type == 'memory' or asset_type == 'data':
        return MemoryAsset(metadata, did)
    elif asset_type == 'bundle':
        return BundleAsset(metadata, did)
    elif asset_type == 'operation':
        return OperationAsset(metadata, did)
    elif asset_type == 'file':
        return FileAsset(metadata, did)
    elif asset_type == 'remote':
        return RemoteAsset(metadata, did)
    return Asset(metadata, did)
