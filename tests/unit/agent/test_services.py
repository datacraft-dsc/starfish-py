
import pytest


from starfish.agent.services import (
    Services,
    SERVICES,
    ALL_SERVICES
)


def test_add_single_default():
    # I want to add a meta service using the default url & version
    services = Services('http://localhost')
    services.add('meta')
    result = services.as_dict
    assert(result)
    assert('meta' in result)
    assert(result['meta']['url'] == 'http://localhost/api/v1/meta')


def test_add_single_version_default():
    # I want to add meta service using the a default version
    services = Services('http://localhost', version='v99')
    services.add('meta')
    result = services.as_dict
    assert(result)
    assert('meta' in result)
    assert(result['meta']['url'] == 'http://localhost/api/v99/meta')
    assert('meta' in services.names)


def test_add_multiple():
    # I want to add only meta and storage services
    services = Services('http://localhost', service_list=['meta', 'storage'])
    result = services.as_dict
    assert(result)
    assert('meta' in result)
    assert(result['meta']['url'] == 'http://localhost/api/v1/meta')
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
