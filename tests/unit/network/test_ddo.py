"""

    Test DDO


"""

import json
import pytest

from starfish.network.ddo import DDO
from starfish.network.did import did_generate_random


def test_create_from_service_list():
    test_url = 'http://localhost'
    ddo = DDO.create(test_url, service_list=['meta', 'trust'])
    assert(ddo)
    #ddo_text = json.dumps(json.loads(ddo.as_text), sort_keys=True, indent=4)
    #print(ddo_text)
    assert('meta' in ddo.service)
    assert(ddo.service['meta']['serviceEndpoint'] == 'http://localhost/api/v1/meta')

    with pytest.raises(TypeError, match=r'Service list must be a list or tuple of service names'):
        ddo = DDO.create(test_url, service_list={
            'bad_name':'meta',
            'invalid': 'trust',
        })

    with pytest.raises(TypeError, match=r'Service list must be a list of type string names'):
        ddo = DDO.create(test_url, service_list=[
            {'type':'meta'},
            {'type': 'trust'},
        ])


def test_create_from_service_list_version():
    test_url = 'http://localhost'
    ddo = DDO.create(test_url, service_list=['meta', 'trust'], version='v99')
    assert(ddo)
    #ddo_text = json.dumps(json.loads(ddo.as_text), sort_keys=True, indent=4)
    #print(ddo_text)
    assert('meta' in ddo.service)
    assert(ddo.service['meta']['serviceEndpoint'] == 'http://localhost/api/v99/meta')


def test_create_all_services():
    test_url = 'http://localhost'
    ddo = DDO.create(test_url)
    assert(ddo)
    assert(len(ddo.service_list) > 5)


def test_basic_init():
    did = did_generate_random()
    ddo = DDO(did)
    assert(ddo)
    assert(ddo.did == did)


def test_import_from_text():
    test_url = 'http://localhost'
    ddo = DDO.create(test_url, service_list=['meta', 'trust'])
    assert(ddo)
    ddo_text = json.dumps(json.loads(ddo.as_text), sort_keys=True, indent=4)
    import_ddo = DDO.import_from_text(ddo_text)
    assert(import_ddo)
    assert(import_ddo.as_text == ddo.as_text)

def test_is_supported_service():
    assert(DDO.is_supported_service('meta'))
    assert(not DDO.is_supported_service('bad-service-name'))


def test_get_did_from_ddo():
    did = did_generate_random()
    test_url = 'http://localhost'
    ddo = DDO.create(test_url, service_list=['meta', 'trust'], did=did)
    assert(ddo)
    assert(ddo.did == did)
    assert(DDO.get_did_from_ddo(ddo) == did)
    assert(DDO.get_did_from_ddo(ddo.as_text) == did)

def test_ddo_checksum():
    test_url = 'http://localhost'
    ddo = DDO.create(test_url, service_list=['meta', 'trust'])
    assert(ddo.checksum == '5da48d1d8b9ad1fdb27400e336dc007dc90a86957dfe1cc179566118d79d9166')
