
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
            'password': config.get('publisher account', 'password')
        }
        self.purchaser_account = {
            'address': config.get('purchaser account', 'address'),
            'password': config.get('purchaser account', 'password')
        }
        self.agent_account = {
            'address': config.get('agent account', 'address'),
            'password': config.get('agent account', 'password')
        }

        items = config.items('squid agent')
        self.squid_config = {}
        for item in items:
            self.squid_config[item[0]] = item[1]

        self.surfer_username=config.get('surfer agent', 'username')
        self.surfer_password=config.get('surfer agent', 'password')
        self.surfer_url=config.get('surfer agent', 'surfer_url')

        self.koi_url=config.get('invoke agent', 'koi_url')
