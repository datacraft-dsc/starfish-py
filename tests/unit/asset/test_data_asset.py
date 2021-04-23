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
    assert(asset.type_name == 'dataset')
    assert(asset.data == TEST_DATA.encode('utf-8'))



def test_set_metadata_content_data():
    metadata = DataAsset.set_metadata_content_data({}, 'test text')
    assert(metadata)
    assert(metadata['contentType'] == 'text/plain')

    metadata = DataAsset.set_metadata_content_data({}, b'test binary data')
    assert(metadata)
    assert(metadata['contentType'] == 'application/octet-stream')

    metadata = DataAsset.set_metadata_content_data({}, b'{"key": "value"}')
    assert(metadata)
    assert(metadata['contentType'] == 'application/json')

    metadata = DataAsset.set_metadata_content_data({}, '{"key": "value"}')
    assert(metadata)
    assert(metadata['contentType'] == 'application/json')


def test_create_from_bytes():
    asset_name = secrets.token_hex(8)
    test_data = secrets.token_bytes(1024)
    asset = DataAsset.create(asset_name, test_data)
    assert(asset)
    assert(isinstance(asset, DataAsset))
    assert(asset.name == asset_name)
    assert(asset.type_name == 'dataset')
    assert(asset.metadata['contentType'] ==  'application/octet-stream')


def test_create_from_text():
    asset_name = secrets.token_hex(8)
    test_data = str(secrets.token_bytes(1024))
    asset = DataAsset.create(asset_name, test_data)
    assert(asset)
    assert(isinstance(asset, DataAsset))
    assert(asset.name == asset_name)
    assert(asset.type_name == 'dataset')
    assert(asset.metadata['contentType'] ==  'text/plain')

def test_create_from_json_text():
    asset_name = secrets.token_hex(8)
    values = {
        'name': 'value',
        'key1': secrets.randbelow(100000)
    }
    test_data = json.dumps(values)
    asset = DataAsset.create(asset_name, test_data)
    assert(asset)
    assert(isinstance(asset, DataAsset))
    assert(asset.name == asset_name)
    assert(asset.type_name == 'dataset')
    assert(asset.metadata['contentType'] ==  'application/json')
