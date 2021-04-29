import json
from typing import Any

from eth_utils import remove_0x_prefix

from starfish.asset.asset_base import AssetBase
from starfish.asset.bundle_asset import BundleAsset
from starfish.asset.data_asset import DataAsset
from starfish.asset.operation_asset import OperationAsset
from starfish.asset.provenance import Provenance
from starfish.asset.remote_data_asset import RemoteDataAsset        # noqa: F401


def create_asset(metadata: [str, dict, bytes], did: str = None, asset: AssetBase = None):
    """
    Create a new asset class based on the metadata. Once created assign
    the metadata to the asset and also the optional did

    :param str metadata_text: metadata text to test and create the correct asset object
    :param str did: optional did to assign to the asset
    :param TAssetBase asset: optional asset object to copy data (only for DataAsset)

    :return: Return an asset class based on the metadata type
    """

    metadata_text = None
    if isinstance(metadata, str):
        metadata_text = metadata
    elif isinstance(metadata, bytes):
        metadata_text = metadata.decode('utf-8')
    elif isinstance(metadata, dict):
        metadata_text = json.dumps(metadata)
    else:
        raise TypeError('metadata must be a string, bytes or dict')

    # now set the metadata for reading
    metadata = json.loads(metadata_text)
    asset_type = metadata.get('type', None)
    data = None
    if asset and hasattr(asset, 'data'):
        data = asset.data

    if asset_type == 'bundle':
        return BundleAsset(metadata_text, did=did)
    elif asset_type == 'operation':
        return OperationAsset(metadata_text, did=did, data=data)
    elif asset_type == 'dataset':
        return DataAsset(metadata_text, did=did, data=data)
    else:
        raise ValueError(f'Unknown asset type {asset_type}')
    return AssetBase(metadata_text, did=did)


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


def create_asset_provenance_publish(asset: AssetBase, agent_did: str = None):
    """

    Add a published provenance data to the asset metadata.
    Calling this method will make the asset 'new'. So the asset_id will change,
    and the asset.did will be set to None.

    :param str agent_did: DID of the agent that this asset will be registered with

    """
    metadata = asset.metadata
    provenance = Provenance(agent_did=agent_did)
    metadata['provenance'] = provenance.create_publish
    return create_asset(metadata, asset=asset)


def create_asset_provenance_invoke(asset: AssetBase, agent_did: str, job_id: str, asset_list: Any, inputs_text: str):
    """

    Add a invoke provenance data to the asset metadata.
    Calling this method will make the asset 'new'. So the asset_id will change,
    and the asset.did will be set to None.

    :param str agent_did: DID of the agent that this asset will be registered with

    """
    metadata = asset.metadata
    provenance = Provenance(agent_did=agent_did, activity_id=job_id, asset_list=asset_list, inputs_text=inputs_text)
    metadata['provenance'] = provenance.create_invoke
    return create_asset(metadata, asset=asset)
