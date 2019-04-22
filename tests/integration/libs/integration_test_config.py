import pathlib
import configparser
from starfish.models.surfer_model import SurferModel

CONFIG_FILE_PATH = pathlib.Path.cwd() / 'tests' / 'integration' / 'config.ini'

class IntegrationTestConfig():
    def __init__(self):

        config = configparser.ConfigParser()
        config.read(CONFIG_FILE_PATH)
        self.keeper_url = config.get('ocean', 'keeper_url')
        self.contracts_path = config.get('ocean', 'contracts_path')
        self.surfer_url = config.get('ocean', 'surfer_url')
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

        self.surfer_username=config.get('surfer', 'username')
        self.surfer_password=config.get('surfer', 'password')
        self.surfer_url=config.get('surfer', 'surfer_url')
        self.authorization=SurferModel.get_authorization_token(self.surfer_url, self.surfer_username, self.surfer_password)


integrationTestConfig = IntegrationTestConfig()
