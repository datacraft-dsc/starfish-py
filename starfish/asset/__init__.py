

from starfish.asset.asset_base import AssetBase
from starfish.asset.data_asset import DataAsset
from starfish.asset.remote_data_asset import RemoteDataAsset
from starfish.asset.bundle_asset import BundleAsset
from starfish.asset.operation_asset import OperationAsset


def create_asset_from_metadata(metadata, did=None):
    """
    Create a new asset class based on the metadata. Once created assign
    the metadata to the asset and also the optional did

    :param dict metadata: metadata to test and create the correct asset object
    :param str did: optional did to assign to the asset

    :return: Return an asset class based on the metadata type
    """

    asset_type = AssetBase.get_asset_type(metadata)

    if asset_type == 'bundle':
        return BundleAsset(metadata, did)
    elif asset_type == 'operation':
        return OperationAsset(metadata, did)
    elif asset_type == 'dataset':
        return DataAsset(metadata, did)
    else:
        raise ValueError(f'Unknown asset type {asset_type}')
    return Asset(metadata, did)
