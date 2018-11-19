"""Config data

"""

import configparser
import logging
import os
import site

from ocean_plastic.constants import (
    KEEPER_CONTRACTS
)

DEFAULT_KEEPER_HOST = 'localhost'
DEFAULT_KEEPER_PORT = 8545
DEFAULT_KEEPER_URL = 'http://localhost:8545'
DEFAULT_KEEPER_PATH = 'contracts'
DEFAULT_GAS_LIMIT = 300000
DEFAULT_NAME_AQUARIUS_URL = 'http://localhost:5000'

NAME_KEEPER_URL = 'keeper.url'
NAME_KEEPER_PATH = 'keeper.path'
NAME_GAS_LIMIT = 'gas_limit'
NAME_AQUARIUS_URL = 'aquarius.url'
NAME_MARKET_ADDRESS = 'market.address'
NAME_AUTH_ADDRESS = 'auth.address'
NAME_TOKEN_ADDRESS = 'token.address'
NAME_DID_REGISTRY_ADDRESS = 'didregistry.address'

environ_names = {
    NAME_KEEPER_URL: ['KEEPER_URL', 'Keeper URL'],
    NAME_KEEPER_PATH: ['KEEPER_PATH', 'Path to the keeper contracts'],
    NAME_GAS_LIMIT: ['GAS_LIMIT', 'Gas limit'],
    NAME_AQUARIUS_URL: ['AQUARIUS_URL', 'Aquarius URL'],
    NAME_MARKET_ADDRESS: ['MARKET_ADDRESS', 'Market address'],
    NAME_AUTH_ADDRESS: ['AUTH_ADDRESS', 'Auth address'],
    NAME_TOKEN_ADDRESS: ['TOKEN_ADDRESS', 'Token address'],
    NAME_DID_REGISTRY_ADDRESS: ['DID_REGISTRY_ADDRESS', 'DIDRegistry address'],
}

config_defaults = {
    KEEPER_CONTRACTS: {
        NAME_KEEPER_URL: DEFAULT_KEEPER_URL,
        NAME_KEEPER_PATH: DEFAULT_KEEPER_PATH,
        NAME_GAS_LIMIT: DEFAULT_GAS_LIMIT,
        NAME_AQUARIUS_URL: DEFAULT_NAME_AQUARIUS_URL,
        NAME_MARKET_ADDRESS: '',
        NAME_AUTH_ADDRESS: '',
        NAME_TOKEN_ADDRESS: '',
        NAME_DID_REGISTRY_ADDRESS: '',
    }
}


class Config(configparser.ConfigParser):

    def __init__(self, filename=None, **kwargs):
        configparser.ConfigParser.__init__(self)

        self.read_dict(config_defaults)
        self._section_name = KEEPER_CONTRACTS
        self._logger = kwargs.get('logger', logging.getLogger(__name__))
        self._logger.debug('Config: loading config file %s', filename)

        if filename:
            with open(filename) as fp:
                text = fp.read()
                self.read_string(text)
        else:
            if 'text' in kwargs:
                self.read_string(kwargs['text'])
        self._load_environ()

    def _load_environ(self):
        for option_name, environ_item in environ_names.items():
            value = os.environ.get(environ_item[0])
            if value is not None:
                self._logger.debug('Config: setting environ %s = %s', option_name, value)
                self.set(self._section_name, option_name, value)

    def set_arguments(self, items):
        for name, value in items.items():
            if value is not None:
                self._logger.debug('Config: setting argument %s = %s', name, value)
                self.set(self._section_name, name, value)

    @property
    def keeper_path(self):
        path = self.get(self._section_name, NAME_KEEPER_PATH)
        if os.path.exists(path):
            pass
        elif os.getenv('VIRTUAL_ENV'):
            path = os.path.join(os.getenv('VIRTUAL_ENV'), 'artifacts')
        else:
            path = os.path.join(site.PREFIXES[0], 'artifacts')
        return path

    # properties

    @property
    def keeper_url(self):
        return self.get(self._section_name, NAME_KEEPER_URL)

    @property
    def gas_limit(self):
        return int(self.get(self._section_name, NAME_GAS_LIMIT))

    @property
    def aquarius_url(self):
        return self.get(self._section_name, NAME_AQUARIUS_URL)

    @property
    def address_list(self):
        return {
            'market': self.get(self._section_name, NAME_MARKET_ADDRESS),
            'auth': self.get(self._section_name, NAME_AUTH_ADDRESS),
            'token': self.get(self._section_name, NAME_TOKEN_ADDRESS),
            'didregistry': self.get(self._section_name, NAME_DID_REGISTRY_ADDRESS),
        }

    # static methods

    @staticmethod
    def get_environ_help():
        result = []
        for option_name, environ_item in environ_names.items():
            # codacy fix
            assert option_name
            result.append("{:20}{:40}".format(environ_item[0], environ_item[1]))
        return "\n".join(result)
