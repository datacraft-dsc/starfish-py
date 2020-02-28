"""

Utils: Data Bundle.

Allow to split up data into 'chunks' and each chunk is an asset, and all of the assets are held in a bundle asset


"""

import math
import re

from starfish.asset import BundleAsset, DataAsset


def decode_readable_size(text):
    sizes = {
        r'([\d\.])\s?t.?': 4,
        r'([\d\.])\s?g.?': 3,
        r'([\d\.])\s?m.?': 2,
        r'([\d\.])\s?k.?': 1,
        r'(\d)\s?b.?': 0,
    }
    for regexp, factor in sizes.items():
        match = re.match(regexp, text, re.IGNORECASE)
        if match:
            return int(float(match.group(1)) * math.pow(1024, factor))
    return None


def register_upload_chunks(remote_agent, name, byte_stream, chunk_size='2 Mb'):
    bundle_asset = BundleAsset.create(name)
    index = 0
    for chunk in byte_stream:
        asset_name = f'{name}:{index}'
        data_asset = DataAsset(asset_name, chunk)
        asset = remote_agent.register_asset(data_asset)
        remote_agent.upload_asset(asset)
        bundle_asset.add(data_asset)
        index += 1
    asset = remote_agent.regsiter_asset(bundle_asset)
    return asset
