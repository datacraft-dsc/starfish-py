
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

        self.keeper_url = config.get('ocean', 'keeper_url')
        self.contracts_path = config.get('ocean', 'contracts_path')
        self.gas_limit = config.get('ocean', 'gas_limit')

        self.publisher_account = {
            'address': config.get('publisher account', 'address'),
            'password': config.get('publisher account', 'password'),
            'keyfile': config.get('publisher account', 'keyfile'),
        }
        self.purchaser_account = {
            'address': config.get('purchaser account', 'address'),
            'password': config.get('purchaser account', 'password'),
            'keyfile': config.get('purchaser account', 'keyfile'),
        }
        self.agent_account = {
            'address': config.get('agent account', 'address'),
            'password': config.get('agent account', 'password'),
            'keyfile': config.get('agent account', 'keyfile'),
        }

        items = config.items('squid agent')
        self.squid_config = {}
        for item in items:
            self.squid_config[item[0]] = item[1]

        self.remote_agent_username=config.get('remote agent', 'username')
        self.remote_agent_password=config.get('remote agent', 'password')
        self.remote_agent_url=config.get('remote agent', 'url')

