import json

from starfish.asset.asset_base import AssetBase
from starfish.asset.data_asset import DataAsset
from starfish.asset.remote_data_asset import RemoteDataAsset
from starfish.asset.bundle_asset import BundleAsset
from starfish.asset.operation_asset import OperationAsset


def create_asset_from_metadata_text(metadata_text, did=None):
    """
    Create a new asset class based on the metadata. Once created assign
    the metadata to the asset and also the optional did

    :param str metadata_text: metadata text to test and create the correct asset object
    :param str did: optional did to assign to the asset

    :return: Return an asset class based on the metadata type
    """

    metadata = json.loads(metadata_text)
    asset_type = AssetBase.get_asset_type(metadata)
    print('asset_type [', asset_type, ']', metadata, type(metadata))
    if asset_type == 'bundle':
        return BundleAsset(metadata, did, metadata_text=metadata_text)
    elif asset_type == 'operation':
        return OperationAsset(metadata, did, metadata_text=metadata_text)
    elif asset_type == 'dataset':
        return DataAsset(metadata, did, metadata_text=metadata_text)
    else:
        raise ValueError(f'Unknown asset type {asset_type}')
    return Asset(metadata, did, metadata_text=metadata_text)
