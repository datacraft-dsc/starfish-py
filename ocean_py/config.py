"""
    Config Class to handle config data and config files

"""

import configparser
import logging
import os
import re
import tempfile

from ocean_py import logger

CONFIG_SECTION_NAME = 'ocean-py'

CONFIG_DEFAULT = """
[ocean-py]
keeper_url = http://localhost:8545
contract_path = artifacts

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
    """ The config class """

    def __init__(self, filename=None, **kwargs):
        """
        Create a new config instance, using a config file, dictionary of values or argument list (kwargs)
        """
        configparser.ConfigParser.__init__(self)

        self.read_string(CONFIG_DEFAULT)
        self._section_name = CONFIG_SECTION_NAME
        values = {}

        if filename:
            if isinstance(filename, str):
                logging.debug('loading config file {}'.format(filename))
                with open(filename) as file_handle:
                    text = file_handle.read()
                    self.read_string(text)
                    values[self._section_name] = kwargs
            elif isinstance(filename, dict):
                logger.debug('loading config from a dict')
                values[self._section_name] = filename
            elif isinstance(filename, Config):
                logger.debug('loading config from another config object')
                for section_name in filename.items():
                    values[section_name[0]] = {}
                    for name, value in filename.items(section_name[0]):
                        values[section_name[0]][name] = value
            else:
                raise TypeError('Invalid type of data passed, can only be a filename or a dict of values')
        else:
            if kwargs:
                logger.debug('loading config from a kwargs')
                values[self._section_name] = kwargs

        if values:
            logger.debug('loading values {}'.format(kwargs))
            self.read_dict(values)
            
        self._read_environ()

    def _read_environ(self):
        """ Read the environment variables and replace them with the config values """
        defaults = configparser.ConfigParser()
        defaults.read_string(CONFIG_DEFAULT)
        for name, value in defaults.items(CONFIG_SECTION_NAME):
            value = os.environ.get(re.sub(r'[^\w]+', '_', name).upper())
            if value is not None:
                logger.debug('setting environ {0} = {1}'.format(name, value))
                self.set(self._section_name, name, value)

    @property
    def as_squid_file(self):
        """
            For compatibility generate a temporary config file, and pass back the filename.
            The config values must conform to the current version of squid-py

        """
        squid = configparser.ConfigParser()
        values = {
            'keeper-contracts': {
                'keeper.url': self.keeper_url,
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
        logger.debug('squid config values {}'.format(values))
        temp_handle = tempfile.mkstemp('_squid.conf', text=True)
        os.close(temp_handle[0])
        filename = temp_handle[1]
        with open(filename, 'w') as file_handle:
            squid.write(file_handle)
        return filename

    @property
    def as_squid_dict(self):
        return {
            'keeper-contracts': {
                'keeper.url': self.keeper_url,
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
        
    @property
    def contract_path(self):
        """return the contract path value"""
        return self.get(self._section_name, 'contract_path')

    @property
    def storage_path(self):
        """ return the storage path"""
        return self.get(self._section_name, 'storage_path')

    @property
    def keeper_url(self):
        """ return the ocean url or ethereum node url"""
        return self.get(self._section_name, 'keeper_url')

    @property
    def gas_limit(self):
        """ return the gas limit """
        return int(self.get(self._section_name, 'gas_limit'))

    @property
    def aquarius_url(self):
        """ return the aquarius server URL """
        return self.get(self._section_name, 'aquarius_url')

    @property
    def brizo_url(self):
        """ return the URL of the brizo server """
        return self.get(self._section_name, 'brizo_url')

    @property
    def secret_store_url(self):
        """ return the secret store URL """
        return self.get(self._section_name, 'secret_store_url')

    @property
    def parity_url(self):
        """ return the parity URL """
        return self.get(self._section_name, 'parity_url')

    @property
    def parity_address(self):
        """ return the parity address """
        return self.get(self._section_name, 'parity_address')

    @property
    def parity_password(self):
        """ return the parity password """
        return self.get(self._section_name, 'parity_password')

