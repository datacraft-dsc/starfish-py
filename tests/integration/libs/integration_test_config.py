
import os
import re

from configparser import (
    ConfigParser,
    ExtendedInterpolation,
)


class IntegrationTestConfig():
    def __init__(self, filename):

        config = ConfigParser(interpolation=ExtendedInterpolation())
        config.read(filename)

        if 'NETWORK_URL' in os.environ:
            config.set('test', 'network_url', os.environ['NETWORK_URL'])

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

        # load in list of agents

        self.agent_list = {}
        for section_name in config.sections():
            match = re.match(r'(\w+)\s+agent', section_name, re.IGNORECASE)
            if match:
                agent_name = match.groups(1)[0]
                self.agent_list[agent_name] = {
                    'url': config.get(section_name, 'url', fallback=None),
                    'did': config.get(section_name, 'did', fallback=None),
                    'username': config.get(section_name, 'username'),
                    'password': config.get(section_name, 'password')
                }


