"""

Utils: Data Bundle.

Allow to split up data into 'chunks' and each chunk is an asset, and all of the assets are held in a bundle asset


"""

import math
import os
import re
from typing import Any

from starfish.agent.agent_base import AgentBase
from starfish.asset import (
    BundleAsset,
    DataAsset
)

# WARNING currently surfer cannot support > 6mb in asset data size
DEFAULT_CHUNK_SIZE = '6mb'


def decode_readable_size(text: str, base_size: int = 1024) -> str:
    sizes = {
        r'(\d)\s?b.?': 0,       # bytes
        r'([\d\.]+)\s?k.?': 1,   # kilobyte
        r'([\d\.]+)\s?m.?': 2,   # megabyte
        r'([\d\.]+)\s?g.?': 3,   # gigabyte
        r'([\d\.]+)\s?t.?': 4,   # terabyte
        r'([\d\.]+)\s?p.?': 5,   # petabyte
        r'([\d\.]+)\s?e.?': 6,   # exabyte
        r'([\d\.]+)\s?z.?': 7,   # zettabyte
        r'([\d\.]+)\s?y.?': 8,   # yottabyte

    }
    for regexp, factor in sizes.items():
        match = re.match(regexp, text, re.IGNORECASE)
        if match:
            value = float(match.group(1))
            return int(value * math.pow(base_size, factor))
    return None


def register_upload_data(remote_agent: AgentBase, name: str, data_stream: Any, chunk_size_value: int = None) -> Any:

    if chunk_size_value is None:
        chunk_size_value = DEFAULT_CHUNK_SIZE

    chunk_size = chunk_size_value
    if isinstance(chunk_size_value, str):
        chunk_size = decode_readable_size(chunk_size_value)
    if not isinstance(chunk_size, int):
        raise ValueError(f'invalid chunk size "{chunk_size_value}", must be int or str')

    bundle_asset = BundleAsset.create(name)
    index = 0
    asset = None
    while True:
        data = data_stream.read(chunk_size)
        if data:
            asset_name = f'{name}:{index}'
            data_asset = DataAsset.create(asset_name, data)
            asset = remote_agent.register_asset(data_asset)
            remote_agent.upload_asset(asset)
            bundle_asset.add(asset_name, asset)
            index += 1
        else:
            break
    if index > 0:
        asset = remote_agent.register_asset(bundle_asset)
    return asset


def register_upload_bundle_file(remote_agent: AgentBase, filename: str, chunk_size: int = None) -> Any:
    if not os.path.exists(filename):
        raise FileNotFoundError(f'Cannot find file {filename}')
    bundle_asset = None
    with open(filename, 'rb') as fp:
        name = f'file: {os.path.basename(filename)}'
        bundle_asset = register_upload_data(remote_agent, name, fp, chunk_size)
    return bundle_asset


def download_bundle_data(remote_agent: AgentBase, bundle_asset: Any, data_stream: Any) -> int:
    size = 0
    for name, asset_id in bundle_asset:
        store_asset = remote_agent.download_asset(asset_id)
        data_stream.write(store_asset.data)
        size += len(store_asset.data)
    return size


def download_bundle_file(remote_agent: AgentBase, bundle_asset: Any, filename: str) -> int:
    if not bundle_asset.is_bundle:
        raise TypeError(f'asset type {bundle_asset.type} is not a bundle asset')
    size = 0
    with open(filename, 'wb') as fp:
        size = download_bundle_data(remote_agent, bundle_asset, fp)
    return size
