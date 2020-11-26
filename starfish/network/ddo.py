"""

    DDO for starfish


"""
import json
import re

from typing import Any

from starfish.network.did import did_generate_random
from starfish.utils.crypto_hash import hash_sha3_256


class DDO:

    SUPPORTED_SERVICES = {
        'meta': {
            'type': 'DEP.Meta',
            'uri': '/meta',
        },
        'storage': {
            'type': 'DEP.Storage',
            'uri': '/assets',
        },
        'invoke': {
            'type': 'DEP.Invoke',
            'uri': '/invoke',
        },
        'market': {
            'type': 'DEP.Market',
            'uri': '/market',
        },
        'trust': {
            'type': 'DEP.Trust',
            'uri': '/trust',
        },
        'auth': {
            'type': 'DEP.Auth',
            'uri': '/auth',
        },
        'collection': {
            'type': 'DEP.Collection',
            'uri': '/collection',
        }
    }

    DEFAULT_VERSION = 'v1'

    @staticmethod
    def create(url, service_list=None, version=None, did=None):
        if service_list:
            if not isinstance(service_list, (tuple, list)):
                raise TypeError('Service list must be a list or tuple of service names')
            elif isinstance(service_list, dict):
                # serice_list is a dict of values
                return DDO(did, service_list)
        else:
            service_list = list(DDO.SUPPORTED_SERVICES.keys())

        ddo = DDO(did)
        for name in service_list:
            if not isinstance(name, str):
                raise TypeError('Service list must be a list of type string names')
            ddo.add_service(name, url=url, version=version)
        return ddo

    @staticmethod
    def import_from_text(text):
        data = json.loads(text)
        return DDO(data['id'], data['service'])

    @staticmethod
    def is_supported_service(name):
        return name in DDO.SUPPORTED_SERVICES

    @staticmethod
    def get_did_from_ddo(ddo_data: Any) -> str:
        if isinstance(ddo_data, str):
            ddo = DDO.import_from_text(ddo_data)
        else:
            ddo = ddo_data
        if ddo:
            return ddo.did

    def __init__(self, did=None, service=None):
        if did is None:
            did = did_generate_random()
        self._did = did
        self._service = {}
        if service:
            if not isinstance(service, (tuple, list)):
                raise TypeError('Service data must be a tuple or list')
            for item in service:
                service_type = item['type']
                name = DDO._supported_service_name_from_type(service_type)
                if not name:
                    name = service_type.lower()
                self._service[name] = item

    def add_service(self, name, endpoint=None, url=None, version=None):
        if not version:
            version = DDO.DEFAULT_VERSION
        if re.search(r'\.', name):
            service_type = name
            # now try to resolve name based on the service type
            name = DDO._supported_service_name_from_type(service_type)
            if not name:
                # if cannot resolve thet set to the new service_type ( orignal name )
                name = service_type

        else:
            # using a template to setup the service
            if name not in DDO.SUPPORTED_SERVICES:
                raise ValueError(f'Invalid service name {name}')
            template = DDO.SUPPORTED_SERVICES[name]
            service_type = f'{template["type"]}.{version}'
            if url:
                endpoint = f'{url}/api/{version}{template["uri"]}'

        if not endpoint:
            raise ValueError('No endpoint or url provided to add a service to the ddo')

        service = {
            'type': service_type,
            'serviceEndpoint': endpoint
        }
        self._service[name] = service

    def remove_service(self, name):
        if name in self._service:
            del self._service[name]
            return True
        return False

    def is_sevice(self, name):
        if name in self._service:
            return True
        return False

    def get_service(self, name):
        if name in self._service:
            return self._service[name]

    def get_service_type(self, service_type):
        for name, item in self._service.items():
            if item['type'] == service_type:
                return item

    @property
    def service_list(self):
        items = []
        for name in sorted(self._service):
            items.append(self._service[name])
        return items

    @property
    def service(self):
        return self._service

    @property
    def did(self):
        return self._did

    @property
    def as_text(self):
        return DDO._as_json(did=self._did, service_list=self.service_list)

    @property
    def checksum(self):
        return hash_sha3_256(DDO._as_json(service_list=self.service_list))

    @staticmethod
    def _as_json(did=None, service_list=None):
        values = {
            '@context': 'https://www.w3.org/2019/did/v1',
        }
        if did:
            values['id'] = did
        if service_list:
            values['service'] = service_list
        return json.dumps(values, sort_keys=True)

    @staticmethod
    def _supported_service_name_from_type(service_type):
        match = re.match(r'^DEP\.(\w+)\.', service_type)
        if match:
            service_name = match.group(1)
            regexp = fr'DEP\.{service_name}'
            for name, item in DDO.SUPPORTED_SERVICES.items():
                if re.match(regexp, item['type']):
                    return name
