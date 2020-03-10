
import os

from configparser import (
    ConfigParser,
    ExtendedInterpolation,
)


class IntegrationTestConfig():
    def __init__(self, filename):

        config = ConfigParser(interpolation=ExtendedInterpolation())
        config.read(filename)

        if 'BARGE_URL' in os.environ:
            config.set('test', 'barge_url', os.environ['BARGE_URL'])

        self.network_url = config.get('network', 'url')

        self.account_1 = {
            'address': config.get('account 1', 'address'),
            'password': config.get('account 1', 'password'),
            'keyfile': config.get('account 1', 'keyfile'),
        }
        self.account_2 = {
            'address': config.get('account 2', 'address'),
            'password': config.get('account 2', 'password'),
            'keyfile': config.get('account 2', 'keyfile'),
        }

        self.remote_agent_username=config.get('remote agent', 'username')
        self.remote_agent_password=config.get('remote agent', 'password')
        self.remote_agent_url=config.get('remote agent', 'url')

