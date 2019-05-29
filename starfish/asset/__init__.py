

from starfish.asset.asset_base import AssetBase
from starfish.asset.memory_asset import MemoryAsset
from starfish.asset.squid_asset import SquidAsset
from starfish.asset.bundle_asset import BundleAsset
from starfish.asset.operation_asset import OperationAsset
from starfish.asset.asset import Asset


def create_asset_from_metadata(metadata, did=None):
    asset_type = ''
    try:
        asset_type = metadata['type']
    except:
        pass
    if asset_type == 'memory':
        return MemoryAsset(metadata, did)
    elif asset_type == 'bundle':
        return BundleAsset(metadata, did)
    elif asset_type == 'squid':
        return SquidAsset(metadata, did)
    elif asset_type == 'operation':
        return OperationAsset(metadata, did)
    return AssetBase(metadata, did)
