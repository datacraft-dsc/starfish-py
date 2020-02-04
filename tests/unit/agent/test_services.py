
import pytest


from starfish.agent.services import (
    Services,
    SERVICES,
    ALL_SERVICES
)


def test_init():
    services = Services('http://localhost')
    services.add('metadata')
    result = services.as_dict
    assert(result)
    assert('metadata' in result)
    assert(result['metadata']['url'] == 'http://localhost/api/v1/meta/data')


    services = Services('http://localhost', version='v99')
    services.add('metadata')
    result = services.as_dict
    assert(result)
    assert('metadata' in result)
    assert(result['metadata']['url'] == 'http://localhost/api/v99/meta/data')
    assert('metadata' in services.names)


    services = Services('http://localhost', service_list=['metadata', 'storage'])
    result = services.as_dict
    assert(result)
    assert('metadata' in result)
    assert(result['metadata']['url'] == 'http://localhost/api/v1/meta/data')
    assert('storage' in result)
    assert(result['storage']['url'] == 'http://localhost/api/v1/assets')


    services = Services('http://localhost', service_list=ALL_SERVICES)
    result = services.as_dict
    assert(result)
    assert(services.names == ALL_SERVICES)

    with pytest.raises(ValueError):
        services.add('bad-name')
