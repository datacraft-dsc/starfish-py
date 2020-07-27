import json
from eth_utils import remove_0x_prefix

from starfish.asset.asset_base import AssetBase
from starfish.asset.bundle_asset import BundleAsset
from starfish.asset.data_asset import DataAsset
from starfish.asset.operation_asset import OperationAsset
from starfish.asset.remote_data_asset import RemoteDataAsset        # noqa: F401


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
    if asset_type == 'bundle':
        return BundleAsset(metadata_text)
    elif asset_type == 'operation':
        return OperationAsset(metadata_text)
    elif asset_type == 'dataset':
        return DataAsset(metadata_text)
    else:
        raise ValueError(f'Unknown asset type {asset_type}')
    return AssetBase(metadata_text)


def is_asset_hash_valid(asset_id, hash_hex):
    """

    :param str asset_id: asset id to check against
    :param str hash_hex: hex string to check
    :return: true if the hash string is the same as the asset_id
    :type: boolean
    """
    if asset_id or hash:
        return remove_0x_prefix(asset_id).lower() == remove_0x_prefix(hash_hex).lower()
    return False
