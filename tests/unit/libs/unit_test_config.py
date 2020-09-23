
from unittest.mock import Mock
import secrets

from tests.unit.libs.unit_test_account import UnitTestAccount

class ConfigEthereum:
    network_url = 'http://test-keeper-url:1234'
    accounts = []


class UnitTestConfig():

    remote_agent_url = 'http://localhost:8080'
    def __init__(self):
        self.ethereum = ConfigEthereum()
        for index in range(0, 2):
            account = self.create_account(secrets.token_hex(32))
            self.ethereum.accounts.append(account)

    def create_account(self, password):
        account = UnitTestAccount(password)
        return account

unitTestConfig = UnitTestConfig()
