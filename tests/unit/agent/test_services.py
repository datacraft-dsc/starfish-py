
import pytest


from starfish.agent.services import (
    Services,
    SERVICES,
    ALL_SERVICES
)


def test_add_single_default():
    # I want to add a metadata service using the default url & version
    services = Services('http://localhost')
    services.add('metadata')
    result = services.as_dict
    assert(result)
    assert('metadata' in result)
    assert(result['metadata']['url'] == 'http://localhost/api/v1/meta/data')


def test_add_single_version_default():
    # I want to add metadata service using the a default version
    services = Services('http://localhost', version='v99')
    services.add('metadata')
    result = services.as_dict
    assert(result)
    assert('metadata' in result)
    assert(result['metadata']['url'] == 'http://localhost/api/v99/meta/data')
    assert('metadata' in services.names)


def test_add_multiple():
    # I want to add only metadata and storage services
    services = Services('http://localhost', service_list=['metadata', 'storage'])
    result = services.as_dict
    assert(result)
    assert('metadata' in result)
    assert(result['metadata']['url'] == 'http://localhost/api/v1/meta/data')
    assert('storage' in result)
    assert(result['storage']['url'] == 'http://localhost/api/v1/assets')


def test_add_all():
    # I want to add all default services
    services = Services('http://localhost', all_services=True)
    result = services.as_dict
    assert(result)
    assert(services.names == ALL_SERVICES)

def test_add_unknown_default():
    # I want to see when a add an unkown service name using the default serivce type
    services = Services('http://localhost', all_services=True)
    result = services.as_dict
    with pytest.raises(ValueError):
        services.add('bad-name')

def test_add_new_service():
    # I want to add a new service uri and service type
    services = Services('http://localhost', all_services=True)
    services.add('test', 'api/v1/test', 'NEW.v1.test')
    result = services.as_dict
    assert(result)
    assert(result['test']['type'] == 'NEW.v1.test')
    assert(result['test']['url'] == 'http://localhost/api/v1/test')
