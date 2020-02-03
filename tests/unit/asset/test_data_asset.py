"""
    test_memory_asset

"""

import secrets
import logging
import json

from starfish.asset import DataAsset




TEST_DATA = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum eu congue odio, vel congue sapien. Morbi ac purus ornare, volutpat elit a, lacinia odio. Integer tempor tellus eget iaculis lacinia. Curabitur aliquam, dui vel vestibulum rhoncus, enim metus interdum enim, in sagittis massa est vel velit. Nunc venenatis commodo libero, vitae elementum nulla ultricies id. Aliquam erat volutpat. Cras eu pretium lacus, quis facilisis mauris. Duis sem quam, blandit id tempor in, porttitor at neque. Cras ut blandit risus. Maecenas vitae sodales neque, eu ultricies nibh.'


def test_init():
    asset = DataAsset.create('test data asset', TEST_DATA)
    assert(asset)
    assert(isinstance(asset, DataAsset))
    assert(asset.data == TEST_DATA.encode('utf-8'))

