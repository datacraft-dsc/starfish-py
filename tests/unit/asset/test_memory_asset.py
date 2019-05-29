"""
    test_memory_asset

"""

import secrets
import logging
import json

from starfish.asset import MemoryAsset

MEMORY_METADATA = {
    'name': 'Memory',
    'type': 'memory',
    'contentType': 'text/plain; charset=utf-8'
}

DATA_METADATA = {
    'name': 'Memory Data',
    'type': 'data',
    'contentType': 'text/plain; charset=utf-8'

}


TEST_DATA = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum eu congue odio, vel congue sapien. Morbi ac purus ornare, volutpat elit a, lacinia odio. Integer tempor tellus eget iaculis lacinia. Curabitur aliquam, dui vel vestibulum rhoncus, enim metus interdum enim, in sagittis massa est vel velit. Nunc venenatis commodo libero, vitae elementum nulla ultricies id. Aliquam erat volutpat. Cras eu pretium lacus, quis facilisis mauris. Duis sem quam, blandit id tempor in, porttitor at neque. Cras ut blandit risus. Maecenas vitae sodales neque, eu ultricies nibh.'


def test_init():
    asset = MemoryAsset(MEMORY_METADATA, None, TEST_DATA)
    assert(asset)
    assert(isinstance(asset, MemoryAsset))
    assert(asset.data == TEST_DATA)


    asset = MemoryAsset(DATA_METADATA, None, TEST_DATA)
    assert(asset)
    assert(isinstance(asset, MemoryAsset))
    assert(asset.data == TEST_DATA)

def test_new():
    asset = MemoryAsset(data=TEST_DATA)
    assert(asset)
    assert(isinstance(asset, MemoryAsset))
    assert(asset.is_asset_type('data'))
    
