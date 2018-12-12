"""Config data

"""

import configparser
import logging
import os
import re
import tempfile
import site

CONFIG_SECTION_NAME = 'ocean-py'

CONFIG_DEFAULT = """
[ocean-py]
ocean_url = http://localhost:8545
contract_path = ./artifacts

secret_store_url = http://localhost:8010
parity_url = http://localhost:9545
parity_address = 0x594d9f933f4f2df6bb66bb34e7ff9d27acc1c019
parity_password = password

aquarius_url = http://localhost:5000
brizo_url = http://localhost:8030

storage_path = squid_py.db

gas_limit = 300000

"""


class Config(configparser.ConfigParser):

    def __init__(self, filename=None, **kwargs):
        configparser.ConfigParser.__init__(self)

        self.read_string(CONFIG_DEFAULT)
        self._section_name = CONFIG_SECTION_NAME

        if filename:
            if isinstance(filename, str):
                with open(filename) as file_handle:
                    text = file_handle.read()
                    self.read_string(text)
            elif isinstance(filename, dict):
                kwargs = filename
            else:
                raise TypeError('Invalid type of data passed, can only be a filename or a dict of values')
        values = {}
        values[self._section_name] = kwargs
        self.read_dict(values)
        self._read_environ()

    def _read_environ(self):
        defaults = configparser.ConfigParser()
        defaults.read_string(CONFIG_DEFAULT)
        for name, value in defaults.items(CONFIG_SECTION_NAME):
            value = os.environ.get(re.sub(r'[^\w]+', '_', name).upper())
            if value is not None:
                # self._logger.debug('Config: setting environ %s = %s', option_name, value)
                self.set(self._section_name, name, value)

    def generate_ocean_config_file(self):
        """
            For compatibility generate a temporary config file, and pass back the filename.
            The config values must conform to the current version of squid-py

        """
        squid= configparser.ConfigParser()
        values = {'keeper-contracts': {
                'keeper.url': self.ocean_url,
                'keeper.path': self.contract_path,
                'secret_store.url': self.secret_store_url,
                'parity.url': self.parity_url,
                'parity.address': self.parity_address,
                'parity.password':  self.parity_password,
                'aquarius.url': self.aquarius_url,
                'brizo.url': self.brizo_url,
                'storage.path': self.storage_path,
            }
        }
        squid.read_dict(values)
        temp_handle = tempfile.mkstemp('_squid.conf', text=True) 
        os.close(temp_handle[0])
        filename = temp_handle[1]
        with open(filename, 'w') as file_handle:
            squid.write(file_handle)
        return filename

    @property
    def contract_path(self):
        return self.get(self._section_name, 'contract_path')

    @property
    def storage_path(self):
        return self.get(self._section_name, 'storage_path')

    @property
    def ocean_url(self):
        return self.get(self._section_name, 'ocean_url')

    @property
    def gas_limit(self):
        return int(self.get(self._section_name, 'gas_limit'))

    @property
    def aquarius_url(self):
        return self.get(self._section_name, 'aquarius_url')

    @property
    def brizo_url(self):
        return self.get(self._section_name, 'brizo_url')

    @property
    def secret_store_url(self):
        return self.get(self._section_name, 'secret_store_url')

    @property
    def parity_url(self):
        return self.get(self._section_name, 'parity_url')

    @property
    def parity_address(self):
        return self.get(self._section_name, 'parity_address')

    @property
    def parity_password(self):
        return self.get(self._section_name, 'parity_password')
